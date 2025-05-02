
# from rest_framework import serializers
# from .models import Parent, Nursery, User
# # from .models import User

# class ParentSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = Parent
#         fields = ['id', 'full_name', 'email', 'phone_number', 'password', 'children_count']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'children_count': {'required': False}
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         email = validated_data['email']
#         user = User.objects.create_user(
#             username=email,
#             email=email,
#             password=password,
#             user_type='parent'
#         )
#         validated_data['children_count'] = validated_data.get('children_count', 0)
#         parent = Parent.objects.create(user=user, **validated_data)
#         return parent

# class NurserySerializer(serializers.ModelSerializer):
#     owner_parent = serializers.SerializerMethodField()

#     class Meta:
#         model = Nursery
#         fields = ['id', 'name', 'location', 'phone', 'capacity', 'owner_parent']

#     def get_owner_parent(self, obj):
#         try:
#             parent = Parent.objects.get(user=obj.user)
#             return ParentSerializer(parent).data
#         except Parent.DoesNotExist:
#             return None

#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             validated_data['user'] = request.user
#         return super().create(validated_data)

# from rest_framework import serializers
# from .models import Parent, Nursery, User

# class ParentSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)  # نضيف email كحقل منفصل للكتابة
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = Parent
#         fields = ['id', 'full_name', 'email', 'phone_number', 'password', 'children_count']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'children_count': {'required': False}
#         }

#     def create(self, validated_data):
#         email = validated_data.pop('email')
#         password = validated_data.pop('password')
#         validated_data['children_count'] = validated_data.get('children_count', 0)
#         user = User.objects.create_user(
#             username=email,
#             email=email,
#             password=password,
#             user_type='parent'
#         )
#         parent = Parent.objects.create(user=user, **validated_data)
#         parent.email = email  # نضيف الـ email للـ Parent
#         parent.save()
#         return parent

# class NurserySerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)  # نضيف email للتسجيل
#     password = serializers.CharField(write_only=True)  # نضيف password للتسجيل

#     class Meta:
#         model = Nursery
#         fields = ['id', 'name', 'location', 'phone', 'capacity', 'email', 'password']

#     def create(self, validated_data):
#         email = validated_data.pop('email')
#         password = validated_data.pop('password')
#         user = User.objects.create_user(
#             username=email,
#             email=email,
#             password=password,
#             user_type='nursery'
#         )
#         nursery = Nursery.objects.create(user=user, **validated_data)
#         return nursery

from rest_framework import serializers
from .models import Parent, Nursery, User

class ParentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'full_name', 'email', 'phone_number', 'password', 'children_count']
        extra_kwargs = {
            'password': {'write_only': True},
            'children_count': {'required': False}
        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data['children_count'] = validated_data.get('children_count', 0)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_type='parent'
        )
        parent = Parent.objects.create(user=user, **validated_data)
        parent.email = email
        parent.save()
        return parent

class NurserySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Nursery
        fields = ['id', 'name', 'location', 'phone', 'capacity', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_type='nursery'
        )
        nursery = Nursery.objects.create(user=user, **validated_data)
        return nursery