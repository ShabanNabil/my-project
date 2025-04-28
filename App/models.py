from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('parent', 'Parent'),
        ('nursery', 'Nursery')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='parent')
    reset_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    children_count = models.IntegerField(default=1)

    def __str__(self):
        return self.full_name

class Nursery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nursery_profile')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    capacity = models.IntegerField(default=20)

    def __str__(self):
        return self.name

class ParentNurseryRelation(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="nursery_relations")
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name="parent_relations")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'nursery')

    def __str__(self):
        return f"{self.parent.full_name} - {self.nursery.name} ({self.status})"

class ParentNote(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="notes")
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.parent.full_name} for {self.nursery.name}"