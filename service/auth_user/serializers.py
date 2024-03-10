from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from service.models import TypeListUser, TypeUser

User = get_user_model()

class CustomUserCreationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        # Создаем пользователя
        user = super().create(validated_data)

        type_user = TypeUser.objects.get(name='physical')
        TypeListUser.objects.create(user=user, type_user=type_user)

        return user