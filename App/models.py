

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

def generate_unique_username():
    return str(uuid.uuid4())[:8]

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not email:
            raise ValueError('The Email field must be set')
        user = self.create_user(email, password, **extra_fields)
        if not user.username:
            user.username = generate_unique_username()
            user.save()
        return user

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('parent', 'Parent'),
        ('nursery', 'Nursery'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True, default='')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='parent')
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    nursery_request = models.TextField(blank=True, default="", verbose_name="Nursery Request Details")
    parent_request = models.TextField(blank=True, default="", verbose_name="Parent Request Details")
    request_status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending', verbose_name="Request Status")
    request_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Request Created At")

    username = models.CharField(
        max_length=150,
        unique=True,
        default=generate_unique_username,
        blank=True,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_unique_username()
        super().save(*args, **kwargs)

class Parent(models.Model):
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'parent'}, null=True, blank=True)
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    address = models.CharField(max_length=255, blank=True, default="Unknown")
    phone_number = models.CharField(max_length=15, unique=True)
    job = models.CharField(max_length=255, blank=True, default="Unknown")

    def __str__(self):
        return self.full_name



class Nursery(models.Model):
    admin_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': 'nursery'})
    name = models.CharField(max_length=255, verbose_name="Nursery Name")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nursery Address")  # optional
    description = models.TextField(blank=True, default="")  # optional
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)  # optional
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='nursery_images/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # للأدمنز والحضانات
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    child_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    father_mother_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True, default='Unknown')
    phone_number = models.CharField(max_length=15, blank=True)
    another_phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=[('male', 'Male'), ('female', 'Female')])



class NurseryParent(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, blank=True)  # حقل جديد
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nursery', 'parent', 'child')  # تعديل عشان يسمح بطلبات مختلفة لكل طفل

    def __str__(self):
        return f"{self.parent.full_name} - {self.nursery.name} - {self.child.child_name if self.child else 'No Child'}"