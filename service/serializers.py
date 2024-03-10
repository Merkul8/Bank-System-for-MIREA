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
        account = super(AccountSerializer, self).create(validated_data)
        
        # Получаем аутентифицированного пользователя
        user = self.context['request'].user
        if user.is_authenticated:
            # Находим или создаем TypeListUser для аутентифицированного пользователя
            type_list_user = TypeListUser.objects.get(user=user)
            
            # Создаем ListAccount с правильным типом пользователя
            ListAccount.objects.create(account=account, type_list_user=type_list_user)
            return account
        else:
            raise serializers.ValidationError("Пользователь не аутентифицирован")


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

