from rest_framework import serializers

import logging

from service.models import (
    TypeListUser,
    TypeUser,
    LegalUser,
    PhisycalUser,
    ListAccount,
    Account,
    Client,
    Payment
)


logger = logging.getLogger(__name__) 


class BaseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['created_at']
        read_only_fields = ['balance', 'account_number']

    def create(self, validated_data):
        account = super().create(validated_data)
        user = self.context['request'].user
        if user.is_authenticated:
            type_list_user = self.get_type_list_user(user)
            list_account = ListAccount.objects.create(account=account, type_list_user=type_list_user)
            logger.info(
                f'Account {account.account_number} was created in ListAccount id {list_account.id}'
            )
            return account
        else:
            raise serializers.ValidationError("Пользователь не аутентифицирован")

    def get_type_list_user(self, user):
        raise NotImplementedError("Subclasses must implement this method.")

class PhysicalUserAccountSerializer(BaseAccountSerializer):
    def get_type_list_user(self, user):
        type_list_user, _ = TypeListUser.objects.get_or_create(user=user, type_user__name='physical')
        return type_list_user

class LegalUserAccountSerializer(BaseAccountSerializer):
    def get_type_list_user(self, user):
        type_list_user, _ = TypeListUser.objects.get_or_create(user=user, type_user__name='legal')
        return type_list_user


class ListAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListAccount
        fields = ['account', 'type_list_user']


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


class PhysicalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhisycalUser
        exclude = ['id','is_stuff', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        TypeListUser.objects.get_or_create(
            user=user, 
            type_user=TypeUser.objects.get(name='physical')
            )
        phisycal_user = PhisycalUser.objects.create(user=user, **validated_data)
        return phisycal_user


class LegalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        exclude = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        TypeListUser.objects.get_or_create(
            user=user, 
            type_user=TypeUser.objects.get(name='legal')
            )
        legal_user = LegalUser.objects.create(user=user, **validated_data)
        return legal_user
    

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'list_account', 'transaction_code', 'amount', 'is_paid_for', 'created_at']
        read_only_fields = ['id', 'transaction_code', 'is_paid_for', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        user.check_payments_and_update_debtor_status()
        self.fields['list_account'].queryset = Payment.get_user_accounts(user)


class UserSerializer(serializers.ModelSerializer):
    typelistuser = TypeListUserSerializer(many=True)
    physicalusers = PhysicalUserSerializer(many=True)
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

