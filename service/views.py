from rest_framework import generics, permissions, viewsets

from service.serializers import (
    ListAccountSerializer,
    UserSerializer,
    LegalUserAccountSerializer,
    PhisycalUserAccountSerializer,
    PhisycalUserSerializer,
    LegalUserSerializer,
    PaymentSerializer
)
from service.models import (
    Client,
    Account,
    ListAccount, 
    PhisycalUser, 
    LegalUser,
    Payment
)



class UserView(generics.ListAPIView):
    """ Список всех пользователей банка """
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PhysicalAccountCreationView(generics.CreateAPIView):
    """ Создание счета. """
    queryset = Account.objects.all()
    serializer_class = PhisycalUserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class LegalAccountCreationView(generics.CreateAPIView):
    """ Создание счета. """
    queryset = Account.objects.all()
    serializer_class = LegalUserAccountSerializer
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
    

class PaymentCreationView(generics.CreateAPIView):
    """ Создание модели платежа. """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

 
class PaymentListView(generics.ListAPIView):
    """ Тестовое представление платежа. """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListAccountListView(generics.ListAPIView):
    """ Тестовое представление для инициализации платежа. Выбор счета для оплаты. """
    serializer_class = ListAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ListAccount.objects.filter(type_list_user__user=self.request.user)

