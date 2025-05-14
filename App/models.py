
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# إدارة المستخدمين (User Manager)
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, name, password, **extra_fields)

# نموذج المستخدم (User)
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('parent', 'Parent'),
        ('nursery', 'Nursery'),
        ('admin', 'Admin'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='parent')  # إضافة user_type
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'admins'

# نموذج الحضانة
class Nursery(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurseries')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='nursery_photos/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nurseries'

# نموذج الوالدين
class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parents')
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name='parents', blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    job = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'parents'

# نموذج الأطفال
class Child(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True, null=True)
    parent_job = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(
        max_length=50,
        choices=[('regular', 'Regular'), ('special', 'Special')],
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.family_name}"

    class Meta:
        db_table = 'children'

# نموذج الزيارات
class Visit(models.Model):
    id = models.AutoField(primary_key=True)
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name='visits')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visit on {self.visit_date} by {self.parent.name}"

    class Meta:
        db_table = 'visits'

# نموذج الإشعارات
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    nursery = models.ForeignKey(Nursery, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notifications'