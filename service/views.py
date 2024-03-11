from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from service.serializers import (
    UserSerializer,
    AccountSerializer,
    PhisycalUserSerializer,
    LegalUserSerializer
)
from service.models import (
    Client,
    Account, 
    PhisycalUser, 
    LegalUser
)



class UserView(generics.ListAPIView):
    """ Список всех пользователей банка """
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class AccountCreationView(generics.CreateAPIView):
    """ Создание счета. """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhisycalUserCRUDSet(viewsets.ModelViewSet):
    """ CRUD операции с моделью физ. лиц. """
    serializer_class = PhisycalUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PhisycalUser.objects.filter(user=self.request.user)
        return queryset


class LegalUserCRUDSet(viewsets.ModelViewSet):
    """ CRUD операции с моделью юр. лиц. """
    serializer_class = LegalUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LegalUser.objects.filter(user=self.request.user)
        return queryset