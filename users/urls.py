from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', views.home, name="home"),
    path("whytherapy/", views.whytherapy, name="whytherapy"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', views.deleteAccount, name='deleteAccount'),
    path('dashboard/contact_patient/', views.therapistDashboardChat, name='therapistDashboardChat'),
    path('dashboard/contact_doctor/', views.patientDashboardChat, name='patientDashboardChat'),
    path("contact/", views.guestContactUs, name="contact"),


]
