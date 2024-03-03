from rest_framework import generics

from service.serializers import (
    UserSerializer,
    UserSerializerTest
)
from service.models import Client



class UserView(generics.RetrieveAPIView):
    """ Личный кабинет пользователя """
    queryset = Client.objects.all().prefetch_related('typelistuser', 'physicalusers', 'legalusers')
    serializer_class = UserSerializer


class UserCreationView(generics.CreateAPIView):
    queryset = Client.objects.all().prefetch_related('physicalusers')
    serializer_class = UserSerializerTest


