from django.urls import path

from service.views import UserView, UserCreationView

urlpatterns = [
    path('users/<int:pk>/', UserView.as_view(), name='user'),
    path('users/sign-up/', UserCreationView.as_view(), name='sign-up'),

]
