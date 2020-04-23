from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/',views.user_registration.as_view(),name='registration'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='token_blacklisted'),
    path('change-password/', views.UpdatePassword.as_view(), name='token_blacklisted'),
    path('login/', views.Login.as_view() ,name='login-login'),
    path('auth-login/', views.AuthLogin.as_view() ,name='auth-login'),
    ]