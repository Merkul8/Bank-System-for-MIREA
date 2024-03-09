from django.urls import path

from service.views import (
    UserView, 
    UserCreationView, 
    UserRUDView,
    AccountCreationView
)

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('users/<int:pk>/', UserRUDView.as_view(), name='user-retrieve'),
    path('users/sign-up/', UserCreationView.as_view(), name='sign-up'),
    path('accounts/create/', AccountCreationView.as_view(), name='add-account'),
]
