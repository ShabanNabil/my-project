# from django.contrib import admin
# from .models import User, Nursery, Parent, Child, Visit, Notification

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email', 'name', 'is_staff', 'is_active', 'created_at']
#     search_fields = ['email', 'name']
#     list_filter = ['is_staff', 'is_active']

# @admin.register(Nursery)
# class NurseryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'admin', 'status', 'created_at']
#     search_fields = ['name', 'address']
#     list_filter = ['status']

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'admin', 'nursery', 'created_at']
#     search_fields = ['name', 'address']
#     list_filter = ['nursery']

# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'family_name', 'parent', 'nursery', 'status', 'created_at']
#     search_fields = ['first_name', 'family_name']
#     list_filter = ['status', 'nursery']

# @admin.register(Visit)
# class VisitAdmin(admin.ModelAdmin):
#     list_display = ['nursery', 'parent', 'visit_date', 'status', 'created_at']
#     search_fields = ['nursery__name', 'parent__name']
#     list_filter = ['status', 'visit_date']

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['title', 'parent', 'nursery', 'is_read', 'created_at']
#     search_fields = ['title', 'message']
#     list_filter = ['is_read']

from django.contrib import admin
from .models import User, Nursery, Parent, Child, Visit, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    list_filter = ['is_staff', 'is_active']

@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin', 'status', 'created_at']
    search_fields = ['name', 'address']
    list_filter = ['status']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin', 'nursery', 'created_at']
    search_fields = ['name', 'address']
    list_filter = ['nursery']

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'family_name', 'parent', 'nursery', 'status', 'created_at']
    search_fields = ['first_name', 'family_name']
    list_filter = ['status', 'nursery']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['nursery', 'parent', 'visit_date', 'status', 'created_at']
    search_fields = ['nursery__name', 'parent__name']
    list_filter = ['status', 'visit_date']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'nursery', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    list_filter = ['is_read']