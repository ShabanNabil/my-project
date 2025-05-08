from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('parents', views.ParentViewSet, basename='parent')
router.register('nurseries', views.NurseryViewSet, basename='nursery')
router.register('admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')
router.register('children', views.ChildViewSet, basename='child')
router.register('visits', views.VisitViewSet, basename='visit')
router.register('notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.SignUpView.as_view(), name='register'),  
    path('login/', views.login_parent_view, name='login'),
    path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    path('login-nursery/', views.login_nursery_view, name='login-nursery'),
    path('login-admin/', views.login_admin_view, name='login-admin'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
]