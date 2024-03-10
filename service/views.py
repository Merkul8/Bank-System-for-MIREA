from rest_framework import generics, permissions

from service.serializers import (
    UserSerializer,
    AccountSerializer,
)
from service.models import Client, Account



class UserView(generics.ListAPIView):
    """ Список всех пользователей банка """
    queryset = Client.objects.all()
    serializer_class = UserSerializer


class AccountCreationView(generics.CreateAPIView):
    """ Создание счета """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# Если счет создается в первый раз, создаем listaccount и typelistuser 
# для данного пользователя, в противном случае добавляем в уже существующие