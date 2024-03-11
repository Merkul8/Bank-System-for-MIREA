from django.urls import path

from service import views
    

urlpatterns = [
    path('users/', views.UserView.as_view(), name='user'),
    path('accounts/create/', views.AccountCreationView.as_view(), name='add-account'),
    path('phisycal/list/', views.PhisycalUserCRUDSet.as_view({'get': 'list'}), name='phisycal-list'),
    path(
        'phisycal/<int:pk>/', 
        views.PhisycalUserCRUDSet.as_view(
        {'get': 'retrieve','put': 'update', 'delete': 'destroy'}
        ), 
        name='phisycal'
        ),
    path('phisycal/create/', views.PhisycalUserCRUDSet.as_view({'post': 'create'}), name='phisycal-creation'),
    path('legal/list/', views.LegalUserCRUDSet.as_view({'get': 'list'}), name='legal-list'),
    path(
        'legal/<int:pk>/', 
        views.LegalUserCRUDSet.as_view(
        {'get': 'retrieve','put': 'update', 'delete': 'destroy'}
        ), 
        name='legal'
        ),
    path('legal/create/', views.LegalUserCRUDSet.as_view({'post': 'create'}), name='legal-creation'),
]
