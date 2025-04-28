from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    
]