from django.urls import path

from . import views

app_name = 'chatbox'

urlpatterns = [
    path('text/<int:work_pk>/', views.new_text, name='new_text'),
    path('<int:pk>', views.inbox_detail, name='inbox_detail'),
    path('', views.inbox, name='inbox'),
]