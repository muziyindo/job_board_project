from django.urls import path
from account import views
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('forget-password/', PasswordResetView.as_view(template_name='account/forget-password.html'), name='forget-password'),
    path('forget-password-response/', views.forget_password_response, name='forget-password-response'),
]
