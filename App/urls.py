

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.SignUpView.as_view(), name='signup'),  # لتسجيل الـ Parent
#     path('login/', views.login_parent_view, name='login'),  # لتسجيل دخول الـ Parent فقط
#     path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     path('login-nursery/', views.login_nursery_view, name='login-nursery'),  # لتسجيل دخول الـ Nursery فقط
#     path('register/', views.NurserySignUpView.as_view(), name='register'),  # لتسجيل الـ Nursery
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register('parents', views.ParentViewSet)
# router.register('nurseries', views.NurseryViewSet)
# router.register('admin/nurseries', views.NurseryAdminViewSet)
# router.register('children', views.ChildViewSet)
# router.register('visits', views.VisitViewSet)
# router.register('notifications', views.NotificationViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.login_parent_view, name='login'),
#     path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     path('login-nursery/', views.login_nursery_view, name='login-nursery'),
#     path('login-admin/', views.login_admin_view, name='login-admin'),
#     path('password-reset/', views.password_reset_request, name='password-reset'),
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register('parents', views.ParentViewSet, basename='parent')  # basename صريح
# router.register('nurseries', views.NurseryViewSet, basename='nursery')  # basename لـ NurseryViewSet
# router.register('admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')  # basename مختلف لـ NurseryAdminViewSet
# router.register('children', views.ChildViewSet, basename='child')  # basename صريح
# router.register('visits', views.VisitViewSet, basename='visit')  # basename صريح
# router.register('notifications', views.NotificationViewSet, basename='notification')  # basename صريح

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.login_parent_view, name='login'),
#     path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     path('login-nursery/', views.login_nursery_view, name='login-nursery'),
#     path('login-admin/', views.login_admin_view, name='login-admin'),
#     path('password-reset/', views.password_reset_request, name='password-reset'),
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
# ]


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
    path('register/', views.SignUpView.as_view(), name='register'),  # أضف هذا السطر
    path('login/', views.login_parent_view, name='login'),
    path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
    path('login-nursery/', views.login_nursery_view, name='login-nursery'),
    path('login-admin/', views.login_admin_view, name='login-admin'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
]