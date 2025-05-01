
# urlpatterns = [
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('app/signup/', views.SignUpView.as_view(), name='signup'),
    path('app/login/', views.login_view, name='login'),
    path('app/signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    path('app/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),  # أضف هذا
    path('app/reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),  # أضف هذا
]