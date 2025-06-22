
# from django.contrib import admin
# from .models import User, Nursery, Parent, Child, Notification, NurseryParent, AdminNurseryRequest, AdminParentRequest

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email', 'user_type', 'created_at']
#     search_fields = ['email']
#     list_filter = ['user_type']

# @admin.register(Nursery)
# class NurseryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'status', 'created_at']
#     search_fields = ['name', 'address']
#     list_filter = ['status']

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_at']
#     search_fields = ['name', 'address']

# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'family_name', 'parent', 'nursery', 'status', 'created_at']
#     search_fields = ['first_name', 'family_name']
#     list_filter = ['status', 'nursery']

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['title', 'is_read', 'created_at']
#     search_fields = ['title', 'message']
#     list_filter = ['is_read']

# @admin.register(NurseryParent)
# class NurseryParentAdmin(admin.ModelAdmin):
#     list_display = ['nursery', 'parent', 'status', 'created_at']
#     search_fields = ['nursery__name', 'parent__name']
#     list_filter = ['status']

# @admin.register(AdminNurseryRequest)
# class AdminNurseryRequestAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'nursery', 'status', 'created_at']
#     search_fields = ['nursery__name']
#     list_filter = ['status']

# @admin.register(AdminParentRequest)
# class AdminParentRequestAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'parent', 'status', 'created_at']
#     search_fields = ['parent__name']
#     list_filter = ['status']


# from django.contrib import admin
# from .models import User, Nursery, Parent, Child, Notification, NurseryParent, AdminNurseryRequest, AdminParentRequest

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email', 'user_type']  # شيلنا created_at لأنه مش موجود
#     search_fields = ['email']
#     list_filter = ['user_type']

# @admin.register(Nursery)
# class NurseryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'address', 'phone']  # شيلنا status وcreated_at، أضفنا phone
#     search_fields = ['name', 'address']
#     # شيلنا list_filter لأن مافيش حقل status

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ['father_mother_name', 'phone']  # غيرنا name لـ father_mother_name، شيلنا created_at
#     search_fields = ['father_mother_name', 'address']

# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'family_name', 'parent', 'nursery']  # شيلنا status وcreated_at
#     search_fields = ['first_name', 'family_name']
#     list_filter = ['parent', 'nursery']  # غيرنا status

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['title', 'is_read', 'created_at']  # created_at موجود هنا
#     search_fields = ['title', 'message']
#     list_filter = ['is_read']

# @admin.register(NurseryParent)
# class NurseryParentAdmin(admin.ModelAdmin):
#     list_display = ['nursery', 'parent', 'status', 'created_at']  # status وcreated_at موجودين هنا
#     search_fields = ['nursery__name', 'parent__father_mother_name']
#     list_filter = ['status']

# @admin.register(AdminNurseryRequest)
# class AdminNurseryRequestAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'nursery', 'status', 'created_at']
#     search_fields = ['nursery__name']
#     list_filter = ['status']

# @admin.register(AdminParentRequest)
# class AdminParentRequestAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'parent', 'status', 'created_at']
#     search_fields = ['parent__father_mother_name']
#     list_filter = ['status']


# from django.contrib import admin
# from .models import User, Nursery, Parent, Child, Notification, NurseryParent

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email', 'user_type', 'nursery_request', 'parent_request', 'request_status', 'request_created_at']
#     search_fields = ['email', 'nursery_request', 'parent_request']
#     list_filter = ['user_type', 'request_status']

# @admin.register(Nursery)
# class NurseryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'address', 'phone']
#     search_fields = ['name', 'address']

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ['father_mother_name', 'phone']
#     search_fields = ['father_mother_name', 'address']

# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'family_name', 'parent', 'nursery']
#     search_fields = ['first_name', 'family_name']
#     list_filter = ['parent', 'nursery']

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['title', 'is_read', 'created_at']
#     search_fields = ['title', 'message']
#     list_filter = ['is_read']

# @admin.register(NurseryParent)
# class NurseryParentAdmin(admin.ModelAdmin):
#     list_display = ['nursery', 'parent', 'status', 'created_at']
#     search_fields = ['nursery__name', 'parent__father_mother_name']
#     list_filter = ['status']


from django.contrib import admin
from .models import User, Nursery, Parent, Child, Notification, NurseryParent

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_type', 'nursery_request', 'parent_request', 'request_status', 'request_created_at']
    search_fields = ['email', 'nursery_request', 'parent_request']
    list_filter = ['user_type', 'request_status']

@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number']  # تغيير من phone إلى phone_number
    search_fields = ['name', 'address']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number']  # تغيير من father_mother_name و phone إلى full_name و phone_number
    search_fields = ['full_name', 'address']  # تحديث search_fields
    list_filter = ['job']  # إضافة filter لو عايزة

# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'family_name', 'parent', 'get_nursery_names']  # استخدام دالة لـ ManyToMany
#     search_fields = ['first_name', 'family_name']
#     list_filter = ['parent']  # nursery مش هيشتغل كـ filter لأنه ManyToMany

#     def get_nursery_names(self, obj):
#         return ", ".join([nursery.name for nursery in obj.nursery.all()])
#     get_nursery_names.short_description = 'Nurseries'

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'father_mother_name', 'parent', 'get_nursery_names']  # تعديل للحقول الجديدة
    search_fields = ['child_name', 'father_mother_name']  # تعديل للبحث
    list_filter = ['parent']  # لسه مناسب

    def get_nursery_names(self, obj):
        return ", ".join([nursery.name for nursery in obj.nursery.all()]) if hasattr(obj, 'nursery') else "No Nurseries"
    get_nursery_names.short_description = 'Nurseries'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    list_filter = ['is_read']

@admin.register(NurseryParent)
class NurseryParentAdmin(admin.ModelAdmin):
    list_display = ['nursery', 'parent', 'status', 'created_at']
    search_fields = ['nursery__name', 'parent__full_name']  # تغيير من father_mother_name إلى full_name
    list_filter = ['status']