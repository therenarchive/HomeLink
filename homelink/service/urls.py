from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('listing_form/', views.new_work, name='new_work'),
    path('<int:pk>/',views.service_detail, name="service_detail"),
    path('search_query/' , views.search_query, name='search_query'),
    path('<int:pk>/edit/',views.edit, name="edit"),
    path('<int:pk>/delete/',views.delete, name="delete"),
    path('<int:pk>/initiate_payment/' , views.initiate_payment, name='initiate_payment'),
    path('payment/verify/', views.verify_payment, name='payment_verify'),
    path('payment/success/<int:pk>/', views.payment_success, name='payment_success'),
]