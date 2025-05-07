# from rest_framework import serializers
# from .models import User, Nursery, Parent, Child, Visit, Notification

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'password', 'created_at', 'is_staff', 'is_active']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         return User.objects.create_user(
#             email=validated_data['email'],
#             name=validated_data['name'],
#             password=validated_data['password']
#         )

# class NurserySerializer(serializers.ModelSerializer):
#     admin = UserSerializer(read_only=True)
#     admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='admin', write_only=True)

#     class Meta:
#         model = Nursery
#         fields = ['id', 'admin', 'admin_id', 'name', 'address', 'phone', 'description', 'photo', 'longitude', 'latitude', 'status', 'created_at', 'updated_at']

# class ParentSerializer(serializers.ModelSerializer):
#     admin = UserSerializer(read_only=True)
#     nursery = NurserySerializer(read_only=True)
#     admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='admin', write_only=True)
#     nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', write_only=True)

#     class Meta:
#         model = Parent
#         fields = ['id', 'admin', 'admin_id', 'nursery', 'nursery_id', 'name', 'address', 'phone', 'job', 'created_at']

# class ChildSerializer(serializers.ModelSerializer):
#     parent = ParentSerializer(read_only=True)
#     nursery = NurserySerializer(read_only=True)
#     parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), source='parent', write_only=True)
#     nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', write_only=True)

#     class Meta:
#         model = Child
#         fields = ['id', 'parent', 'parent_id', 'nursery', 'nursery_id', 'first_name', 'family_name', 'address', 'birth_date', 'gender', 'phone', 'alternative_phone', 'parent_job', 'status', 'created_at', 'updated_at']

# class VisitSerializer(serializers.ModelSerializer):
#     nursery = NurserySerializer(read_only=True)
#     parent = ParentSerializer(read_only=True)
#     nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', write_only=True)
#     parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), source='parent', write_only=True)

#     class Meta:
#         model = Visit
#         fields = ['id', 'nursery', 'nursery_id', 'parent', 'parent_id', 'visit_date', 'status', 'created_at', 'updated_at']

# class NotificationSerializer(serializers.ModelSerializer):
#     nursery = NurserySerializer(read_only=True)
#     parent = ParentSerializer(read_only=True)
#     nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', allow_null=True, write_only=True)
#     parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), source='parent', allow_null=True, write_only=True)

#     class Meta:
#         model = Notification
#         fields = ['id', 'nursery', 'nursery_id', 'parent', 'parent_id', 'title', 'message', 'is_read', 'created_at', 'updated_at']


from rest_framework import serializers
from .models import User, Nursery, Parent, Child, Visit, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_staff', 'is_active', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

class NurserySerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='admin', write_only=True)

    class Meta:
        model = Nursery
        fields = ['id', 'admin', 'admin_id', 'name', 'address', 'phone', 'description', 
                  'photo', 'longitude', 'latitude', 'status', 'created_at', 'updated_at']

class ParentSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    nursery = NurserySerializer(read_only=True)
    admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='admin', write_only=True)
    nursery_id = serializers.PrimaryKeyRelatedField(
        queryset=Nursery.objects.all(), source='nursery', write_only=True, required=False
    )

    class Meta:
        model = Parent
        fields = ['id', 'admin', 'admin_id', 'nursery', 'nursery_id', 'name', 'address', 
                  'phone', 'job', 'created_at', 'updated_at']

class ChildSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(read_only=True)
    nursery = NurserySerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), source='parent', write_only=True)
    nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', write_only=True)

    class Meta:
        model = Child
        fields = ['id', 'parent', 'parent_id', 'nursery', 'nursery_id', 'first_name', 
                  'family_name', 'address', 'birth_date', 'gender', 'phone', 
                  'alternative_phone', 'parent_job', 'religion', 'type', 'status', 
                  'created_at', 'updated_at']

class VisitSerializer(serializers.ModelSerializer):
    nursery = NurserySerializer(read_only=True)
    parent = ParentSerializer(read_only=True)
    nursery_id = serializers.PrimaryKeyRelatedField(queryset=Nursery.objects.all(), source='nursery', write_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), source='parent', write_only=True)

    class Meta:
        model = Visit
        fields = ['id', 'nursery', 'nursery_id', 'parent', 'parent_id', 'visit_date', 
                  'status', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    nursery = NurserySerializer(read_only=True)
    parent = ParentSerializer(read_only=True)
    nursery_id = serializers.PrimaryKeyRelatedField(
        queryset=Nursery.objects.all(), source='nursery', allow_null=True, write_only=True
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Parent.objects.all(), source='parent', allow_null=True, write_only=True
    )

    class Meta:
        model = Notification
        fields = ['id', 'nursery', 'nursery_id', 'parent', 'parent_id', 'title', 
                  'message', 'is_read', 'created_at', 'updated_at']