from django.urls import path

from service.views import (
    UserView,
    AccountCreationView,
)

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('accounts/create/', AccountCreationView.as_view(), name='add-account'),
]
