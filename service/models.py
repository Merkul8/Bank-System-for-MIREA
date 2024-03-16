from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from phonenumber_field.modelfields import PhoneNumberField
import uuid
import logging

from service.constants import (
    OWNERSHIP_CHOICES,
    GENDER_CHOICES,
    USER_TYPE_CHOICES
)

logger = logging.getLogger(__name__) 


class Client(AbstractUser):
    is_debtor = models.BooleanField(default=False, verbose_name='Статус должника')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="client_groups",
        related_query_name="client",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="client_user_permissions",
        related_query_name="client",
    )

    def check_payments_and_update_debtor_status(self):
        # Проверяем, есть ли у пользователя платежи с is_paid_for=False
        unpaid_payments = Payment.objects.filter(list_account__type_list_user__user=self, is_paid_for=False)
        if not unpaid_payments.exists():
            # Если нет неоплаченных платежей, обновляем статус is_debtor на False
            self.is_debtor = True
            self.save()


class TypeUser(models.Model):
    name = models.CharField(verbose_name = 'Тип пользователя', max_length=100, choices=USER_TYPE_CHOICES)

    def __str__(self) -> str:
        return self.name


class TypeListUser(models.Model):
    type_user = models.ForeignKey(TypeUser, verbose_name = 'Тип пользователя', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name='typelistuser')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.type_user}'


class PhisycalUser(models.Model):
    lastname = models.CharField(verbose_name = 'Фамилия', max_length=100, null=False)
    firstname = models.CharField(verbose_name = 'Имя', max_length=100, null=False)
    patronymic = models.CharField(verbose_name = 'Отчество', max_length=100, null=False)
    birth_day = models.DateField(verbose_name = 'Дата рождения', null=False)
    address = models.CharField(verbose_name = 'Адрес прописки', max_length=100, null=False)
    number = PhoneNumberField(verbose_name = 'Номер телефона', null=False)
    gender = models.CharField(verbose_name = 'Пол', max_length=5, choices=GENDER_CHOICES, null=False)
    photo = models.ImageField(verbose_name = 'Аватар', upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    is_stuff = models.BooleanField(verbose_name = 'Сотрудник банка', default=False)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name='physicalusers')

    def __str__(self) -> str:
        return f'{self.user.username} {str(self.number)}'
    

class LegalUser(models.Model):
    org_name = models.CharField(verbose_name = 'Название организации', max_length=100, null=False)
    address = models.CharField(verbose_name = 'Адрес организации', max_length=100, null=False)
    boss_full_name = models.CharField(verbose_name = 'ФИО директора', max_length=100, null=False)
    accountant_full_name = models.CharField(verbose_name = 'ФИО главного бухгалтера', max_length=100, null=False)
    number = PhoneNumberField(verbose_name = 'Контактный номер', null=False)
    form_of_ownership = models.CharField(
        verbose_name = 'Форма организации', 
        max_length=100, 
        choices=OWNERSHIP_CHOICES, 
        null=False
    )
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name='legalusers')
    
    def __str__(self) -> str:
        return f'{self.user.username} {str(self.number)}'


class AccountType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип карты')
    account_type = models.ForeignKey('AccountType', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    account_number = models.CharField(
        verbose_name = 'Номер счета',
        max_length=100,
        unique=True,
        blank=True,
        help_text='Номер счета (для чековых начинается с символов “101-“, для сберегательных – с символов “102-”)'
    )
    created_at = models.DateTimeField(verbose_name = 'Дата и время создания', auto_now_add=True)
    balance = models.DecimalField(verbose_name = 'Баланс', max_digits=10, decimal_places=2, default=0)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{str(self.account_number[:3])} {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

    def save(self, *args, **kwargs):
        # Генерация уникального номера счета
        if not self.account_number:
            accounts = ('Дебетовый', 'Кредитный',)
            prefix = '101-' if self.account_type.name in accounts else '102-'
            self.account_number = prefix + str(uuid.uuid4())
        super().save(*args, **kwargs)
        logger.info(f'Account {self.pk} was created with {self.account_number}')


class ListAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    type_list_user = models.ForeignKey(
        TypeListUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='type_list_user_account'
        )

    def __str__(self) -> str:
        return f'{self.type_list_user.user.username} {self.account}'


class Payment(models.Model):
    transaction_code = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Код транзакции')
    list_account = models.ForeignKey(ListAccount, on_delete=models.CASCADE, related_name='payment_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма платежа')
    is_paid_for = models.BooleanField(verbose_name = 'Статус оплаты', default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f'{self.list_account.account.account_type} {self.is_paid_for}'
    
    @staticmethod
    def get_user_accounts(user):
        return ListAccount.objects.filter(type_list_user__user=user)