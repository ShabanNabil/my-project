# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
# from .views import get_nurseries, get_child_profile, request_nursery_join

# router = DefaultRouter()
# router.register(r'parents', views.ParentViewSet, basename='parent')  # أزلنا api/ من النمط
# router.register(r'nurseries', views.NurseryViewSet, basename='nursery')
# router.register(r'admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')
# router.register(r'children', views.ChildViewSet, basename='child')
# router.register(r'notifications', views.NotificationViewSet, basename='notification')

# urlpatterns = [
#     path('api/', include(router.urls)),  # api/ هنا بيضاف لكل النماط
#     path('register/', views.SignUpView.as_view(), name='register'),
#     # path('login/', views.login_parent_view, name='login'),
#     # path('signup-nursery/', views.NurserySignUpView.as_view(), name='signup-nursery'),
#     # path('login-nursery/', views.login_nursery_view, name='login-nursery'),
#     # path('login-admin/', views.login_admin_view, name='login-admin'),
#     path('password-reset/', views.password_reset_request, name='password-reset'),
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     # path('reset-password/parent/', views.ParentResetPasswordView.as_view(), name='reset-password-parent'),
#     path('nurseries/', get_nurseries, name='get-nurseries'),
#     path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
#     path('nursery-dashboard/<int:nursery_id>/', views.NurseryDashboardView.as_view(), name='nursery-dashboard'),
#     path('request-nursery-join/', request_nursery_join, name='request-nursery-join'),
#     path('child-profile/', get_child_profile, name='child-profile'),
# ]



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
# from .views import get_nurseries, get_child_profile, request_nursery_join

# router = DefaultRouter()
# router.register(r'parents', views.ParentViewSet, basename='parent')
# router.register(r'nurseries', views.NurseryViewSet, basename='nursery')
# router.register(r'admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')
# router.register(r'children', views.ChildViewSet, basename='child')
# router.register(r'notifications', views.NotificationViewSet, basename='notification')

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('password-reset/', views.password_reset_request, name='password-reset'),
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('nurseries/', get_nurseries, name='get-nurseries'),
#     path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
#     path('nursery-dashboard/<int:nursery_id>/', views.NurseryDashboardView.as_view(), name='nursery-dashboard'),
#     path('request-nursery-join/', request_nursery_join, name='request-nursery-join'),
#     path('child-profile/', get_child_profile, name='child-profile'),
# ]



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'parents', views.ParentViewSet, basename='parent')
# router.register(r'nurseries', views.NurseryViewSet, basename='nursery')
# router.register(r'admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')
# router.register(r'children', views.ChildViewSet, basename='child')
# router.register(r'notifications', views.NotificationViewSet, basename='notification')

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('signup/parent/', views.ParentSignUpView.as_view(), name='parent-signup'),
#     path('signup/nursery/', views.NurserySignUpView.as_view(), name='nursery-signup'),
#     path('login/parent/', views.parent_login, name='parent-login'),
#     path('login/nursery/', views.nursery_login, name='nursery-login'),
#     path('login/admin/', views.admin_login, name='admin-login'),
#     path('password-reset/', views.password_reset_request, name='password-reset'),
#     path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
#     path('nurseries/', views.get_nurseries, name='get-nurseries'),
#     path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
#     path('nursery-dashboard/<int:nursery_id>/', views.NurseryDashboardView.as_view(), name='nursery-dashboard'),
#     path('request-nursery-join/', views.request_nursery_join, name='request-nursery-join'),
#     path('child-profile/', views.get_child_profile, name='child-profile'),
# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AdminNurseryDashboard, AdminParentDashboard
router = DefaultRouter()
router.register(r'parents', views.ParentViewSet, basename='parent')
router.register(r'nurseries', views.NurseryViewSet, basename='nursery')
router.register(r'admin/nurseries', views.NurseryAdminViewSet, basename='admin-nursery')
router.register(r'children', views.ChildViewSet, basename='child')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/parent/', views.ParentSignUpView.as_view(), name='parent-signup'),  #تمام
    path('signup/nursery/', views.NurserySignUpView.as_view(), name='nursery-signup'),#تمام
    path('login/parent/', views.parent_login, name='parent-login'),#تمام 
    path('login/nursery/', views.nursery_login, name='nursery-login'),#تمام
    path('login/admin/', views.admin_login, name='admin-login'),#تمام
    # path('password-reset/', views.password_reset_request, name='password-reset'),#تمام
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),#تمام

    path('nursery-information/', views.NurseryInformationView.as_view(), name='nursery-information'),#تمام 
    #////////////////////////////////////////////////////////////////////////
    path('nursery-home/', views.NurseryHomeView.as_view(), name='nursery-home'),
    path('nursery-edit/', views.NurseryEditView.as_view(), name='nursery-edit'),
    path('search-nurseries/', views.NurserySearchView.as_view(), name='nursery-search'),
    path('admin-nursery-dashboard/<int:nursery_id>/', AdminNurseryDashboard.as_view(), name='admin-nursery-dashboard'),
    path('admin-nursery-dashboard/', AdminNurseryDashboard.as_view(), name='admin-nursery-dashboard-list'),
    path('admin-parent-dashboard/<int:parent_id>/', AdminParentDashboard.as_view(), name='admin-parent-dashboard'),
    path('admin-parent-dashboard/', AdminParentDashboard.as_view(), name='admin-parent-dashboard-list'),
    path('nurseries/', views.get_nurseries, name='get-nurseries'),#// ده اللى بيجيب الحضانات المقبولة تسمع فى السيرش 
    
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-dashboard/<int:nursery_id>/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    # path('api/approved-nurseries/', views.ApprovedNurseriesView.as_view(), name='approved-nurseries'),
    # path('nursery-dashboard/<int:nursery_id>/', views.NurseryDashboardView.as_view(), name='nursery-dashboard'),
    path('nursery-dashboard/<int:nursery_id>/', views.NurseryDashboardView.as_view(), name='nursery-dashboard'),



    # path('request-nursery-join/', views.request_nursery_join, name='request-nursery-join'),
    path('child-profile/', views.get_child_profile, name='child-profile'),
    path('add-child/', views.add_child, name='add-child'), 
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('nursery-details/<int:nursery_id>/', views.get_nursery_details, name='get-nursery-details'),  
    path('nursery-info/', views.get_nursery_info, name='get-nursery-info'),
    path('update-nursery-info/', views.update_nursery_info, name='update-nursery-info'),
    path('get-dashboard/', views.get_dashboard, name='get-dashboard'),
    path('dashboard-action/', views.dashboard_action, name='dashboard-action'),
    path('get-parent-requests/', views.get_parent_requests, name='get-parent-requests'),
    path('update-parent-request/<int:parent_id>/', views.update_parent_request, name='update-parent-request'),
    path('get-nursery-requests/', views.get_nursery_requests, name='get-nursery-requests'),
  
]

