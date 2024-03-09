from rest_framework import serializers

import logging

from service.models import (
    TypeListUser,
    TypeUser,
    LegalUser,
    PhisycalUser,
    ListAccount,
    Account,
    Client
)


logger = logging.getLogger(__name__) 


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ['created_at']
        read_only_fields = ['balance', 'account_number']

    def create(self, validated_data):
        account_id = validated_data.get('account_id')
        
        user = self.context['request'].user
        account = ListAccount.objects.create(account_id=account_id, type_list_user=user)
        return account


class ListAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = ListAccount
        fields = ['account']


class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeUser
        fields = ['name']


class TypeListUserSerializer(serializers.ModelSerializer):
    type_user = serializers.StringRelatedField()
    type_list_user_account = ListAccountSerializer(many=True)

    class Meta:
        model = TypeListUser
        fields = ['type_user', 'type_list_user_account']


class PhisycalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhisycalUser
        exclude = ['user']


class LegalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    typelistuser = TypeListUserSerializer(many=True)
    physicalusers = PhisycalUserSerializer(many=True)
    legalusers = LegalUserSerializer(many=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'username', 
            'typelistuser', 
            'physicalusers', 
            'legalusers'
            )


class UserCreationSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Client и PhisycalUser """
    physicalusers = PhisycalUserSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'username',
            'password',
            'physicalusers'
        ]
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        physicalusers = validated_data.pop('physicalusers')
        user = Client.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
            logger.info(f'{physicalusers} and type - {type(physicalusers)}')
        [PhisycalUser.objects.create(user=user, **physicaluser) for physicaluser in physicalusers]

        type_user = TypeUser.objects.get(name='physical')
        TypeListUser.objects.create(user=user, type_user=type_user)
        return user