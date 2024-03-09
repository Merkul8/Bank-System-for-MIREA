from rest_framework import generics, permissions

from service.serializers import (
    UserSerializer,
    UserCreationSerializer,
    AccountSerializer
)
from service.models import Client, Account



class UserView(generics.ListAPIView):
    """ Список всех пользователей банка """
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreationView(generics.CreateAPIView):
    """ Представление создания пользователя, поумолчанию создается аккаунт для физ. лица """
    queryset = Client.objects.all()
    serializer_class = UserCreationSerializer


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Все возможные операции с пользователем (retrieve, update, destroy) """
    queryset = Client.objects.all()
    serializer_class = UserSerializer


class AccountCreationView(generics.CreateAPIView):
    """ Создание счета """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# Если счет создается в первый раз, создаем listaccount и typelistuser 
# для данного пользователя, в противном случае добавляем в уже существующие