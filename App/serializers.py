# from rest_framework import serializers
# from django.core.validators import RegexValidator
# from .models import User, Nursery, Parent, Child, Notification

# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(write_only=True, required=True)  

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'user_type', 'reset_token', 'username', 'name', 'first_name']
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 8},
#             'reset_token': {'write_only': True},
#             'username': {'required': False},
#             'first_name': {'read_only': True}  
#         }

#     def create(self, validated_data):
#         name = validated_data.pop('name', '')  
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             user_type=validated_data.get('user_type'),
#             username=validated_data.get('email', validated_data['email']),
#             first_name=name  
#         )
#         return user

# class NurserySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nursery
#         fields = '__all__'

# class ParentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Parent
#         fields = '__all__'
#         extra_kwargs = {
#             'phone': {'validators': [RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]}
#         }

# class ChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Child
#         fields = '__all__'

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'



# from rest_framework import serializers
# from django.core.validators import RegexValidator
# from .models import User, Nursery, Parent, Child, Notification, NurseryParent

# class UserSerializer(serializers.ModelSerializer):
#     father_mother_name = serializers.CharField(write_only=True, required=True, source='first_name')

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'user_type', 'reset_token', 'username', 'father_mother_name', 'first_name', 'nursery_request', 'parent_request', 'request_status', 'request_created_at']
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 8},
#             'reset_token': {'write_only': True},
#             'username': {'required': False},
#             'first_name': {'read_only': True},
#             'nursery_request': {'required': False},
#             'parent_request': {'required': False},
#             'request_status': {'required': False},
#             'request_created_at': {'read_only': True}
#         }

#     def create(self, validated_data):
#         validated_data.pop('father_mother_name', None)
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             user_type=validated_data.get('user_type'),
#             username=validated_data.get('email', validated_data['email']),
#             first_name=validated_data.get('first_name', '')
#         )
#         # يمكن تضيفي قيم default للـ request fields لو محتاجاها
#         user.nursery_request = validated_data.get('nursery_request', '')
#         user.parent_request = validated_data.get('parent_request', '')
#         user.request_status = validated_data.get('request_status', 'pending')
#         user.save()
#         return user

# class NurserySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nursery
#         fields = '__all__'
#         extra_kwargs = {
#             'image': {'required': False}
#         }

# class ParentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Parent
#         fields = '__all__'
#         extra_kwargs = {
#             'phone': {'validators': [RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]}
#         }

# class ChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Child
#         fields = '__all__'
#         extra_kwargs = {
#             'phone': {'required': False},
#             'religion': {'required': False}
#         }

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'

# class NurseryParentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NurseryParent
#         fields = '__all__'



from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User, Nursery, Parent, Child, Notification, NurseryParent
import uuid
class UserSerializer(serializers.ModelSerializer):
    father_mother_name = serializers.CharField(write_only=True, required=True, source='first_name')
    phone_number = serializers.CharField(
        write_only=True,
        required=False,
        validators=[RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'user_type', 'reset_token', 'username', 'father_mother_name', 'first_name', 'nursery_request', 'parent_request', 'request_status', 'request_created_at', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'reset_token': {'write_only': True},
            'username': {'required': False},
            'first_name': {'read_only': True},
            'nursery_request': {'required': False},
            'parent_request': {'required': False},
            'request_status': {'required': False},
            'request_created_at': {'read_only': True},
            'phone_number': {'write_only': True, 'required': False}
        }

    def validate_email(self, value):
        # تحقق إن الـ email مش موجود مسبقًا
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        validated_data['first_name'] = validated_data.pop('father_mother_name', '')

        if 'username' not in validated_data or not validated_data['username']:
            email = validated_data['email']
            username_base = email.split('@')[0]
            unique_suffix = str(uuid.uuid4())[:8]
            validated_data['username'] = f"{username_base}_{unique_suffix}"

        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                user_type=validated_data.get('user_type'),
                username=validated_data['username'],
                first_name=validated_data.get('first_name', '')
            )
            user.nursery_request = validated_data.get('nursery_request', '')
            user.parent_request = validated_data.get('parent_request', '')
            user.request_status = validated_data.get('request_status', 'pending')
            user.save()
            validated_data['phone_number'] = phone_number
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create user: {str(e)}")

class NurserySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nursery
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        extra_kwargs = {
            'phone': {'validators': [RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]}
        }

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        extra_kwargs = {
            'phone': {'required': False},
            'religion': {'required': False}
        }

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NurseryParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseryParent
        fields = '__all__'