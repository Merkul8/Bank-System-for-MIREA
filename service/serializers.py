from rest_framework import serializers

from service.models import (
    TypeListUser,
    TypeUser,
    LegalUser,
    PhisycalUser,
    ListAccount,
    Account,
    Client
)


class AccountSerializer(serializers.ModelSerializer):
    account_type = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = '__all__'


class ListAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = ListAccount
        fields = ['id', 'account']


class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeUser
        fields = ['name']


class TypeListUserSerializer(serializers.ModelSerializer):
    type_user = serializers.StringRelatedField()
    type_list_user_account = ListAccountSerializer(many=True, read_only=True)

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
    typelistuser = TypeListUserSerializer(many=True, read_only=True)
    physicalusers = PhisycalUserSerializer(many=True, read_only=True)
    legalusers = LegalUserSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = (
            'username', 
            'typelistuser', 
            'physicalusers', 
            'legalusers'
            )
        
class UserSerializerTest(serializers.ModelSerializer):
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
            print(f'{physicalusers} and type - {type(physicalusers)}')
        for physicaluser in physicalusers:
            PhisycalUser.objects.create(user=user, **physicaluser)
        return user