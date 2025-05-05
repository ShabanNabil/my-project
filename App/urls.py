

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),  # لتسجيل الـ Parent
    path('login/', views.login_parent_view, name='login'),  # لتسجيل دخول الـ Parent فقط
    path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    path('login-nursery/', views.login_nursery_view, name='login-nursery'),  # لتسجيل دخول الـ Nursery فقط
    path('register/', views.NurserySignUpView.as_view(), name='register'),  # لتسجيل الـ Nursery
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
]