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
#     path('', welcome, name='welcome'),
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('app/', include('App.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def welcome(request):
    return JsonResponse({"message": "Welcome to Nursery API. Available endpoints: /app/login/ (Parent), /app/login-nursery/ (Nursery), /app/signup/ (Parent), /app/register/ (Nursery)"}, status=200)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    path('app/', include('App.urls')),  # رابط لتطبيق App
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # إعدادات الـ media