from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .forms import LoginForm

from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('workers_json/', views.workers_json, name='workers_json'),
    path('nearby_map/', views.nearby_map, name='nearby_map'),
    path('contact/', views.contact, name='contact'),
    path('featured/', views.featured, name='featured')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)