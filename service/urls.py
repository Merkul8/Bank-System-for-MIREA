from django.urls import path

from service import views
    

urlpatterns = [
    path('users/', views.UserView.as_view(), name='user'),
    path('accounts/create/', views.AccountCreationView.as_view(), name='add-account'),
    path('phisycal/create/', views.PhisycalUserCreationView.as_view(), name='add-phisycal'),
    path('phisycal/list/', views.PhisycalListByUserView.as_view(), name='phisycal-list'),
    path('phisycal/<int:pk>/', views.PhisycalUserRUDView.as_view(), name='phisycal'),
]
