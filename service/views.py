from rest_framework import generics, permissions

from service.serializers import (
    UserSerializer,
    AccountSerializer,
    PhisycalUserSerializer
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


class PhisycalUserCreationView(generics.CreateAPIView):
    """ Создание физ. лица по пользователю. """
    queryset = PhisycalUser.objects.all()
    serializer_class = PhisycalUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhisycalListByUserView(generics.ListAPIView):
    """ Список всех зарегистрированных физ. лиц по пользователю. """
    serializer_class = PhisycalUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PhisycalUser.objects.filter(user=self.request.user)
        return queryset


class PhisycalUserRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Обновление, удаление и просмотр данных по физическому лицу. """
    queryset = PhisycalUser.objects.all()
    serializer_class = PhisycalUserSerializer
    permission_classes = [permissions.IsAuthenticated]
