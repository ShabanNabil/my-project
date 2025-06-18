

from django.contrib.auth.models import AbstractUser
import django.db.models as models  # استخدام اسم مختلف

# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('parent', 'Parent'),
#         ('nursery', 'Nursery'),
#         ('admin', 'Admin'),
#     )
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='parent')
#     reset_token = models.CharField(max_length=100, null=True, blank=True)
    
#     # إضافة حقول الطلبات بدل الجداول المنفصلة
#     nursery_request = models.TextField(blank=True, default="", verbose_name="Nursery Request Details")
#     parent_request = models.TextField(blank=True, default="", verbose_name="Parent Request Details")
#     request_status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending', verbose_name="Request Status")
#     request_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Request Created At")
    
#     def __str__(self):
#         return self.email

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('parent', 'Parent'),
        ('nursery', 'Nursery'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)  # إضافة unique=True هنا
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='parent')
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    nursery_request = models.TextField(blank=True, default="", verbose_name="Nursery Request Details")
    parent_request = models.TextField(blank=True, default="", verbose_name="Parent Request Details")
    request_status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending', verbose_name="Request Status")
    request_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Request Created At")

    USERNAME_FIELD = 'email'  # إضافة هنا
    REQUIRED_FIELDS = []  # لتجنب مشاكل مع الـ email

    def __str__(self):
        return self.email

class Parent(models.Model):
    admin_id = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'parent'})  # إزالة primary_key=True
    father_mother_name = models.CharField(max_length=255, verbose_name="Father/Mother Name")
    address = models.CharField(max_length=255, blank=True, default="Unknown")
    phone = models.CharField(max_length=15, unique=True)
    job = models.CharField(max_length=255, blank=True, default="Unknown")

    def __str__(self):
        return self.father_mother_name

class Nursery(models.Model):
    admin_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': 'nursery'})
    name = models.CharField(max_length=255, verbose_name="Nursery Name")
    address = models.CharField(max_length=255, verbose_name="Nursery Address")
    description = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=15, unique=True)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='nursery_images/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'  # القيمة الافتراضية
    )

    def __str__(self):
        return self.name
class Notification(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    nursery = models.ForeignKey(Nursery, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    religion = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')))
    address = models.CharField(max_length=255, blank=True, default="Unknown")
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    guardian_job = models.CharField(max_length=255, blank=True, default="Unknown")

    def __str__(self):
        return f"{self.first_name} {self.family_name}"

class NurseryParent(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nursery', 'parent')

    def __str__(self):
        return f"{self.parent.father_mother_name} - {self.nursery.name}"