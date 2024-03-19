from django.urls import path

from service import views
    

urlpatterns = [
    path('users/', views.UserView.as_view(), name='user'),
    path('accounts/create/phy/', views.PhysicalAccountCreationView.as_view(), name='add-phy-account'),
    path('accounts/create/leg/', views.LegalAccountCreationView.as_view(), name='add-leg-account'),
    path('phisycal/list/', views.PhysicalUserCRUDSet.as_view({'get': 'list'}), name='phisycal-list'),
    path(
        'phisycal/<int:pk>/', 
        views.PhysicalUserCRUDSet.as_view(
        {'get': 'retrieve','put': 'update', 'delete': 'destroy'}
        ), 
        name='phisycal'
        ),
    path('phisycal/create/', views.PhysicalUserCRUDSet.as_view({'post': 'create'}), name='phisycal-creation'),
    path('legal/list/', views.LegalUserCRUDSet.as_view({'get': 'list'}), name='legal-list'),
    path(
        'legal/<int:pk>/', 
        views.LegalUserCRUDSet.as_view(
        {'get': 'retrieve','put': 'update', 'delete': 'destroy'}
        ), 
        name='legal'
        ),
    path('legal/create/', views.LegalUserCRUDSet.as_view({'post': 'create'}), name='legal-creation'),
    path('payments/create/', views.PaymentCreationView.as_view(), name='payment-creation'),
    path('payments/list/', views.PaymentListView.as_view(), name='payment-list'),
    path('list-accounts/list/', views.ListAccountListView.as_view(), name='list-account'),
]
