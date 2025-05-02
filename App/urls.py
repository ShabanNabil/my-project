
# urlpatterns = [
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('app/signup/', views.SignUpView.as_view(), name='signup'),
#     path('app/login/', views.login_view, name='login'),
#     path('app/signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     path('app/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),  # أضف هذا
#     path('app/reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),  # أضف هذا
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('app/signup/', views.SignUpView.as_view(), name='signup'),
#     path('app/login-parent/', views.login_parent_view, name='login-parent'),  # للوالدين
#     path('app/signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     path('app/login-nursery/', views.login_nursery_view, name='login-nursery'),  # للحضانات
#     path('app/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('app/reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login-parent/', views.login_parent_view, name='login-parent'),  # للوالدين
    path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    path('login-nursery/', views.login_nursery_view, name='login-nursery'),  # للحضانات
    path('login/', views.login_view, name='login'),  # أضفنا ده عشان يدعم /app/login/
    path('register/', views.NurserySignUpView.as_view(), name='register'),  # أضفنا ده عشان يدعم /register/
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
]