

# from rest_framework import serializers
# from django.core.validators import RegexValidator
# from .models import User, Nursery, Parent, Child, Notification, NurseryParent
# import uuid
# from datetime import datetime

# class UserSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(write_only=True, required=True, source='first_name')  # تغيير من father_mother_name إلى full_name
#     phone_number = serializers.CharField(
#         write_only=True,
#         required=False,
#         validators=[RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]
#     )

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'user_type', 'reset_token', 'username', 'full_name', 'first_name', 'nursery_request', 'parent_request', 'request_status', 'request_created_at', 'phone_number']
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 8},
#             'reset_token': {'write_only': True},
#             'username': {'required': False},
#             'first_name': {'read_only': True},
#             'nursery_request': {'required': False},
#             'parent_request': {'required': False},
#             'request_status': {'required': False},
#             'request_created_at': {'read_only': True},
#             'phone_number': {'write_only': True, 'required': False}
#         }

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Email already exists.")
#         return value

#     def create(self, validated_data):
#         print(f"Validated data before pop: {validated_data}")
#         phone_number = validated_data.pop('phone_number', None)
#         # validated_data['first_name'] = validated_data.pop('full_name', validated_data.pop('father_mother_name', ''))  # دعم الاثنين للتوافق
#         validated_data['first_name'] = validated_data.get('full_name', '')  # استخدام full_name فقط
#         print(f"Validated data after pop: {validated_data}")


#         if 'username' not in validated_data or not validated_data['username']:
#             email = validated_data['email']
#             username_base = email.split('@')[0]
#             unique_suffix = str(uuid.uuid4())[:8]
#             validated_data['username'] = f"{username_base}_{unique_suffix}"

#         try:
#             user = User.objects.create_user(
#                 email=validated_data['email'],
#                 password=validated_data['password'],
#                 user_type=validated_data.get('user_type'),
#                 username=validated_data['username'],
#                 first_name=validated_data.get('first_name', '')
#             )
#             print(f"Created user password: {user.password}")
#             user.nursery_request = validated_data.get('nursery_request', '')
#             user.parent_request = validated_data.get('parent_request', '')
#             user.request_status = validated_data.get('request_status', 'pending')
#             user.save()
#             validated_data['phone_number'] = phone_number
#             return user
#         except Exception as e:
#             print(f"Error in create: {e}")
#             raise serializers.ValidationError(f"Failed to create user: {str(e)}")

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
#             'phone_number': {'validators': [RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]}  # تغيير من phone إلى phone_number
#         }


# class ChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Child
#         fields = ['id', 'parent', 'child_name', 'date_of_birth', 'father_mother_name', 'job', 'address', 'phone_number', 'another_phone_number', 'gender']
#         extra_kwargs = {
#             'address': {'required': False, 'default': 'Unknown'},
#             'job': {'required': False},
#             'phone_number': {'required': False},
#             'another_phone_number': {'required': False'}
#             'gender': {'required': False}
#         }

#     date_of_birth = serializers.DateField(
#         input_formats=['%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d'],  # الصيغ المسموح بيها
#         required=True
#     )

#     def validate_date_of_birth(self, value):
#         # تحويل التاريخ لـ YYYY-MM-DD زي ما بيحب الـ model
#         return value  # الـ DateField هيحول تلقائيًا



# class NurseryParentSerializer(serializers.ModelSerializer):
#     nursery = NurserySerializer()
#     parent = ParentSerializer()
#     child = ChildSerializer()

#     class Meta:
#         model = NurseryParent
#         fields = ['id', 'nursery', 'parent', 'child', 'status', 'created_at']
from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User, Nursery, Parent, Child, Notification, NurseryParent
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=True, source='first_name')  # تغيير من father_mother_name إلى full_name
    phone_number = serializers.CharField(
        write_only=True,
        required=False,
        validators=[RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'user_type', 'reset_token', 'username', 'full_name', 'first_name', 'nursery_request', 'parent_request', 'request_status', 'request_created_at', 'phone_number']
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
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        print(f"Validated data before pop: {validated_data}")
        phone_number = validated_data.pop('phone_number', None)
        validated_data['first_name'] = validated_data.get('full_name', '')  # استخدام full_name فقط
        print(f"Validated data after pop: {validated_data}")

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
            print(f"Created user password: {user.password}")
            user.nursery_request = validated_data.get('nursery_request', '')
            user.parent_request = validated_data.get('parent_request', '')
            user.request_status = validated_data.get('request_status', 'pending')
            user.save()
            validated_data['phone_number'] = phone_number
            return user
        except Exception as e:
            print(f"Error in create: {e}")
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
            'phone_number': {'validators': [RegexValidator(r'^\d{10,11}$', message='Phone number must be 10-11 digits.')]}  # تغيير من phone إلى phone_number
        }

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'parent', 'child_name', 'date_of_birth', 'father_mother_name', 'job', 'address', 'phone_number', 'another_phone_number', 'gender']
        extra_kwargs = {
            'address': {'required': False, 'default': 'Unknown'},
            'job': {'required': False},
            'phone_number': {'required': False},
            'another_phone_number': {'required': False},
            'gender': {'required': False}
        }

    date_of_birth = serializers.DateField(
        input_formats=['%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d'],
        required=True
    )

    def validate_date_of_birth(self, value):
        if isinstance(value, str):
            try:
                date_obj = datetime.strptime(value, '%d-%m-%Y')
                logger.info(f"Parsed date_of_birth: {value} to {date_obj.date()}")
                return date_obj.date()
            except ValueError:
                raise serializers.ValidationError("Date must be in dd-MM-yyyy, MM/dd/yyyy, or YYYY-MM-DD format")
        return value

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'is_read', 'title', 'message', 'nursery', 'user', 'parent', 'created_at']  # الحقول المستخدمة في الكود

class NurseryParentSerializer(serializers.ModelSerializer):
    nursery = NurserySerializer()
    parent = ParentSerializer()
    child = ChildSerializer()

    class Meta:
        model = NurseryParent
        fields = ['id', 'nursery', 'parent', 'child', 'status', 'created_at']