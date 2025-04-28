from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Parent, Nursery, ParentNurseryRelation, ParentNote

# تسجيل موديل User (لأنه يورث من AbstractUser)
admin.site.register(User, UserAdmin)

# تسجيل باقي الموديلات
admin.site.register(Parent)
admin.site.register(Nursery)
admin.site.register(ParentNurseryRelation)
admin.site.register(ParentNote)