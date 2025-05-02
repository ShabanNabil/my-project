# """
# URL configuration for Nursery_project project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


# """
# URL configuration for project project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from App.views import ParentViewSet, NurseryViewSet, login_view  

# router = DefaultRouter()
# router.register('parents', ParentViewSet)
# router.register('nurseries', NurseryViewSet)

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('api/', include(router.urls)),
# #     path('login/', login_view, name='login'),  
# #     path('app/', include('App.urls')),
# #     # path('', include('accounts.urls')),
# # ]

# from django.http import JsonResponse

# def welcome(request):
#     return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/, /app/signup/, /app/signup-nursery/"}, status=200)

# urlpatterns = [
#     path('', welcome, name='welcome'),  # مسار الـ root
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('app/', include('App.urls')),
# ]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/login/', login_view, name='login'),
#     path('api/password-reset-request/', password_reset_request, name='password_reset_request'),
#     path('api/password-reset-confirm/', password_reset_confirm, name='password_reset_confirm'),
# ]

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from App.views import ParentViewSet, NurseryViewSet

# router = DefaultRouter()
# router.register('parents', ParentViewSet)
# router.register('nurseries', NurseryViewSet)

# from django.http import JsonResponse

# def welcome(request):
#     return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/, /app/signup/, /app/register/"}, status=200)

# urlpatterns = [
#     path('', welcome, name='welcome'),  # مسار الـ root
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('app/', include('App.urls')),
# ]

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from App.views import ParentViewSet, NurseryViewSet

# router = DefaultRouter()
# router.register('parents', ParentViewSet)
# router.register('nurseries', NurseryViewSet)

# from django.http import JsonResponse

# def welcome(request):
#     return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/ (Parent), /app/login-nursery/ (Nursery), /app/signup/ (Parent), /app/register/ (Nursery)"}, status=200)

# urlpatterns = [
#     path('', welcome, name='welcome'),  # مسار الـ root
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('app/', include('App.urls')),
# ]

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from App.views import ParentViewSet, NurseryViewSet

# router = DefaultRouter()
# router.register('parents', ParentViewSet)
# router.register('nurseries', NurseryViewSet)

# from django.http import JsonResponse

# def welcome(request):
#     return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/ (Parent & Nursery), /app/signup/ (Parent), /app/register/ (Nursery)"}, status=200)

# urlpatterns = [
#     path('', welcome, name='welcome'),
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('app/', include('App.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from App.views import ParentViewSet, NurseryViewSet

router = DefaultRouter()
router.register('parents', ParentViewSet)
router.register('nurseries', NurseryViewSet)

from django.http import JsonResponse

def welcome(request):
    return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/ (Parent), /app/login-nursery/ (Nursery), /app/signup/ (Parent), /app/register/ (Nursery)"}, status=200)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('app/', include('App.urls')),
]