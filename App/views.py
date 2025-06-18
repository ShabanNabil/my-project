from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User, Nursery, Parent, Child, Notification, NurseryParent
from .serializers import UserSerializer, NurserySerializer, ParentSerializer, ChildSerializer, NotificationSerializer
import uuid
from django.db.utils import IntegrityError
from django.db import transaction, models
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action

# دالة مساعدة لإنشاء الإشعارات
def create_notification(recipient, title, message, is_nursery=False):
    kwargs = {'is_read': False, 'title': title, 'message': message}
    if is_nursery:
        kwargs['nursery'] = recipient
    else:
        kwargs['parent'] = recipient
    Notification.objects.create(**kwargs)


class ParentSignUpView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        user_data = {
            'father_mother_name': request.data.get('father_mother_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'user_type': 'parent'
        }
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response({
                'error': 'Failed to create user',
                'code': 'INVALID_USER_DATA',
                'details': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if User.objects.filter(email=user_data['email']).exists():
                return Response({
                    'error': 'Email already exists',
                    'code': 'DUPLICATE_EMAIL'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = user_serializer.save()  # حفظ المستخدم أولاً
            parent_data = {
                'admin_id': user,  # ربط الكائن User مباشرة
                'father_mother_name': user_data['father_mother_name'],
                'address': request.data.get('address', 'Unknown'),
                'phone': request.data.get('phone', ''),
                'job': request.data.get('job', '')
            }
            if not parent_data['phone']:
                user.delete()
                return Response({
                    'error': 'Phone number is required',
                    'code': 'MISSING_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)

            if Parent.objects.filter(phone=parent_data['phone']).exists():
                user.delete()
                return Response({
                    'error': 'Phone number already exists',
                    'code': 'DUPLICATE_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)

            parent = Parent.objects.create(**parent_data)  # حفظ الـ Parent

            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'parent_id': parent.id,
                'user_type': 'parent'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            if 'user' in locals():
                user.delete()
            return Response({
                'error': f'Invalid data: {str(e)}',
                'code': 'INVALID_DATA'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if 'user' in locals():
                user.delete()
            if 'parent' in locals():
                parent.delete()
            return Response({
                'error': f'Failed to create parent: {str(e)}',
                'code': 'SERVER_ERROR'
            }, status=status.HTTP_400_BAD_REQUEST)
        

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def parent_login(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return Response({
#             'error': 'Email and password are required',
#             'code': 'MISSING_CREDENTIALS'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # البحث عن المستخدم بناءً على الـ email
#         try:
#             user = User.objects.get(email=email, user_type='parent')
#         except User.DoesNotExist:
#             return Response({
#                 'error': 'Invalid credentials or not a parent',
#                 'code': 'INVALID_CREDENTIALS'
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         # التحقق باستخدام الـ username المحفوظ
#         user = authenticate(request, username=user.username, password=password)
#         if user is None:
#             return Response({
#                 'error': 'Invalid credentials. Check password or username.',
#                 'code': 'INVALID_CREDENTIALS',
#                 'debug': {'username_used': user.username}  # للتحقق
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         # إنشاء التوكن
#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             'success': True,
#             'token': str(refresh.access_token),
#             'user_id': user.id,
#             'user_type': 'parent',
#             'message': 'Login successful for parent'
#         }
#         return Response(response_data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({
#             'error': f'Failed to login: {str(e)}',
#             'code': 'SERVER_ERROR'
#         }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def parent_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error': 'Email and password are required',
            'code': 'MISSING_CREDENTIALS'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, user_type='parent')
        if not check_password(password, user.password):  # تحقق مباشر
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'user_type': 'parent',
            'message': 'Login successful for parent'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials or not a parent',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)
class NurserySignUpView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        # استخراج البيانات من الـ request
        full_name = request.data.get('full_name')
        if not full_name:
            return Response({
                'error': 'Full name is required',
                'code': 'MISSING_FULL_NAME'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'father_mother_name': full_name,
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'user_type': 'nursery',
            'phone_number': request.data.get('phone_number')
        }
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response({
                'error': 'Failed to create user',
                'code': 'INVALID_USER_DATA',
                'details': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_serializer.save()
            nursery_data = {
                'admin_id': user.id,
                'name': full_name,
                'phone': user_data.get('phone_number'),
                'address': request.data.get('location', 'Unknown'),
                'description': request.data.get('description', ''),
                'longitude': request.data.get('longitude', 0.0),
                'latitude': request.data.get('latitude', 0.0),
                'status': 'pending',
                'image': request.data.get('image', None)
            }
            if not nursery_data['phone']:
                user.delete()
                return Response({
                    'error': 'Phone number is required',
                    'code': 'MISSING_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Nursery.objects.filter(phone=nursery_data['phone']).exists():
                user.delete()
                return Response({
                    'error': 'Phone number already exists',
                    'code': 'DUPLICATE_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)

            nursery_serializer = NurserySerializer(data=nursery_data)
            if not nursery_serializer.is_valid():
                user.delete()
                return Response({
                    'error': 'Failed to create nursery',
                    'code': 'INVALID_NURSERY_DATA',
                    'details': nursery_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            nursery = nursery_serializer.save()
            user.nursery_request = f"New nursery registration for {nursery.name}"
            user.request_status = 'pending'
            user.save()
            create_notification(
                nursery,
                title="New Nursery Request",
                message=f"A new nursery {nursery.name} has submitted a request.",
                is_nursery=True
            )
            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'nursery_id': nursery.admin_id.id,  # نستخدم admin_id.id
                'nursery_status': nursery.status,
                'user_type': 'nursery'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            user.delete()
            return Response({
                'error': f'Failed to create user or nursery: {str(e)}',
                'code': 'UNIQUE_CONSTRAINT_FAILED'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'error': f'Invalid data: {str(e)}',
                'code': 'INVALID_DATA'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            user.delete()
            return Response({
                'error': f'Failed to create nursery: {str(e)}',
                'code': 'SERVER_ERROR'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def nursery_login(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return Response({
#             'error': 'Email and password are required',
#             'code': 'MISSING_CREDENTIALS'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email, user_type='nursery')
#         nursery = Nursery.objects.get(admin_id=user)
#         if nursery.status != 'accepted':
#             return Response({
#                 'error': 'Nursery is not accepted',
#                 'code': 'NURSERY_NOT_ACCEPTED'
#             }, status=status.HTTP_403_FORBIDDEN)

#         user = authenticate(request, username=email, password=password)
#         if user is None:
#             return Response({
#                 'error': 'Invalid credentials',
#                 'code': 'INVALID_CREDENTIALS'
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             'success': True,
#             'token': str(refresh.access_token),
#             'user_id': user.id,
#             'nursery_id': nursery.admin_id.id,
#             'nursery_status': nursery.status,
#             'user_type': 'nursery',
#             'message': 'Login successful for nursery'
#         }
#         return Response(response_data, status=status.HTTP_200_OK)
#     except (User.DoesNotExist, Nursery.DoesNotExist):
#         return Response({
#             'error': 'Invalid credentials or not a nursery',
#             'code': 'INVALID_CREDENTIALS'
#         }, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
@permission_classes([AllowAny])
def nursery_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error': 'Email and password are required',
            'code': 'MISSING_CREDENTIALS'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, user_type='nursery')
        nursery = Nursery.objects.get(admin_id=user)
        if nursery.status != 'accepted':
            return Response({
                'error': 'Nursery is not accepted',
                'code': 'NURSERY_NOT_ACCEPTED'
            }, status=status.HTTP_403_FORBIDDEN)

        if not check_password(password, user.password):
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'nursery_id': nursery.admin_id.id,
            'nursery_status': nursery.status,
            'user_type': 'nursery',
            'message': 'Login successful for nursery'
        }, status=status.HTTP_200_OK)
    except (User.DoesNotExist, Nursery.DoesNotExist):
        return Response({
            'error': 'Invalid credentials or not a nursery',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)
# تسجيل دخول (Admin)
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error': 'Email and password are required',
            'code': 'MISSING_CREDENTIALS'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, user_type='admin')
        if not (user.is_staff and user.is_superuser):
            return Response({
                'error': 'User is not an admin',
                'code': 'NOT_ADMIN'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'user_type': 'admin',
            'message': 'Login successful for admin',
            'nursery_requests': user.nursery_request,
            'parent_requests': user.parent_request,
            'request_status': user.request_status,
            'request_created_at': user.request_created_at
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials or not an admin',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nurseries(request):
    nurseries = Nursery.objects.filter(status='accepted')
    serializer = NurserySerializer(nurseries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        token = str(uuid.uuid4())
        user.reset_token = token
        user.save()
        reset_link = f"https://your-frontend.com/reset-password?token={token}"
        send_mail(
            'Password Reset Request',
            f'Click this link to reset your password: {reset_link}',
            'from@yourdomain.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Email not found', 'code': 'EMAIL_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e), 'code': 'SERVER_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        reset_token = request.data.get('reset_token')
        user_type = request.data.get('user_type', None)

        try:
            user = User.objects.get(email=email, reset_token=reset_token)
            if user_type == 'parent' and not Parent.objects.filter(admin=user).exists():
                return Response({
                    'error': 'User is not a parent',
                    'code': 'NOT_PARENT'
                }, status=status.HTTP_404_NOT_FOUND)

            user.set_password(new_password)
            user.reset_token = None
            user.save()
            return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid email or token',
                'code': 'INVALID_TOKEN'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e),
                'code': 'SERVER_ERROR'
            }, status=status.HTTP_400_BAD_REQUEST)

class ParentViewSet(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return Parent.objects.all()
        return Parent.objects.filter(admin=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        parent = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        admin_user = User.objects.get(user_type='admin')
        admin_user.parent_request = f"Request for {parent.father_mother_name}"
        admin_user.request_status = status
        admin_user.save()

        create_notification(
            parent,
            title=f"Parent {status.capitalize()}",
            message=f"Your account has been {status} by the admin."
        )

        return Response({'success': True, 'message': f'Parent status updated to {status}'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not (request.user.is_staff and request.user.is_superuser):
            return Response({'error': 'Only admins can delete parents', 'code': 'NOT_ADMIN'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True, 'message': 'Parent deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class NurseryViewSet(ModelViewSet):
    queryset = Nursery.objects.all()
    serializer_class = NurserySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return Nursery.objects.all()
        return Nursery.objects.filter(admin=user)

class NurseryAdminViewSet(ModelViewSet):
    queryset = Nursery.objects.all()
    serializer_class = NurserySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Nursery.objects.all()

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        nursery = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        nursery.status = status
        nursery.save()

        admin_user = User.objects.get(user_type='admin')
        admin_user.nursery_request = f"Request for {nursery.name}"
        admin_user.request_status = status
        admin_user.save()

        create_notification(
            nursery,
            title=f"Nursery {status.capitalize()}",
            message=f"Your nursery {nursery.name} has been {status} by the admin.",
            is_nursery=True
        )

        return Response({'success': True, 'message': f'Nursery status updated to {status}'}, status=status.HTTP_200_OK)

class ChildViewSet(ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return Child.objects.all()
        return Child.objects.filter(nursery__admin=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        child = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        child.status = status
        child.save()

        create_notification(
            child.parent,
            title=f"Child {status.capitalize()}",
            message=f"Your child {child.first_name} {child.family_name} has been {status} by the nursery."
        )

        return Response({'success': True, 'message': f'Child status updated to {status}'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(parent=Parent.objects.get(admin=self.request.user))

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            models.Q(nursery__admin=user) | models.Q(parent__admin=user)
        ).distinct()

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'success': True, 'message': 'Notification marked as read'}, status=status.HTTP_200_OK)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        admin_user = request.user
        users_with_requests = User.objects.filter(
            models.Q(nursery_request__isnull=False, nursery_request__ne='') | 
            models.Q(parent_request__isnull=False, parent_request__ne='')
        ).exclude(user_type='admin')

        pending_parents = [user for user in users_with_requests if user.user_type == 'parent' and user.request_status == 'pending']
        accepted_parents = [user for user in users_with_requests if user.user_type == 'parent' and user.request_status == 'accepted']
        rejected_parents = [user for user in users_with_requests if user.user_type == 'parent' and user.request_status == 'rejected']

        pending_parent_serializer = ParentSerializer([Parent.objects.get(admin=user) for user in pending_parents], many=True)
        accepted_parent_serializer = ParentSerializer([Parent.objects.get(admin=user) for user in accepted_parents], many=True)
        rejected_parent_serializer = ParentSerializer([Parent.objects.get(admin=user) for user in rejected_parents], many=True)

        pending_nurseries = [user for user in users_with_requests if user.user_type == 'nursery' and user.request_status == 'pending']
        accepted_nurseries = [user for user in users_with_requests if user.user_type == 'nursery' and user.request_status == 'accepted']
        rejected_nurseries = [user for user in users_with_requests if user.user_type == 'nursery' and user.request_status == 'rejected']

        pending_nursery_serializer = NurserySerializer([Nursery.objects.get(admin=user) for user in pending_nurseries], many=True)
        accepted_nursery_serializer = NurserySerializer([Nursery.objects.get(admin=user) for user in accepted_nurseries], many=True)
        rejected_nursery_serializer = NurserySerializer([Nursery.objects.get(admin=user) for user in rejected_nurseries], many=True)

        return Response({
            'pending_parents': pending_parent_serializer.data,
            'accepted_parents': accepted_parent_serializer.data,
            'rejected_parents': rejected_parent_serializer.data,
            'pending_nurseries': pending_nursery_serializer.data,
            'accepted_nurseries': accepted_nursery_serializer.data,
            'rejected_nurseries': rejected_nursery_serializer.data
        }, status=status.HTTP_200_OK)

class NurseryDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nursery_id):
        try:
            nursery = Nursery.objects.get(id=nursery_id, admin=request.user)
            pending_requests = NurseryParent.objects.filter(nursery=nursery, status='pending')
            accepted_requests = NurseryParent.objects.filter(nursery=nursery, status='accepted')
            rejected_requests = NurseryParent.objects.filter(nursery=nursery, status='rejected')

            pending_parents = [req.parent for req in pending_requests]
            accepted_parents = [req.parent for req in accepted_requests]
            rejected_parents = [req.parent for req in rejected_requests]

            pending_serializer = ParentSerializer(pending_parents, many=True)
            accepted_serializer = ParentSerializer(accepted_parents, many=True)
            rejected_serializer = ParentSerializer(rejected_parents, many=True)

            return Response({
                'nursery': NurserySerializer(nursery).data,
                'pending_parents': pending_serializer.data,
                'accepted_parents': accepted_serializer.data,
                'rejected_parents': rejected_serializer.data
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            return Response({'message': 'Nursery not found or you do not have access'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, nursery_id):
        parent_id = request.data.get('parent_id')
        action = request.data.get('action')  # 'accept' or 'reject'

        try:
            nursery = Nursery.objects.get(id=nursery_id, admin=request.user)
            parent = Parent.objects.get(id=parent_id)
            request_obj = NurseryParent.objects.get(nursery=nursery, parent=parent)

            if action == 'accept':
                request_obj.status = 'accepted'
                request_obj.save()
                message = f"Your request to join {nursery.name} has been accepted."
            elif action == 'reject':
                request_obj.status = 'rejected'
                request_obj.save()
                message = f"Your request to join {nursery.name} has been rejected."
            else:
                return Response({'message': 'Invalid action', 'code': 'INVALID_ACTION'}, status=status.HTTP_400_BAD_REQUEST)

            create_notification(
                parent,
                title=f"Join Request {action.capitalize()}",
                message=message
            )

            return Response({'message': f'Parent request {action}ed'}, status=status.HTTP_200_OK)
        except (Nursery.DoesNotExist, Parent.DoesNotExist, NurseryParent.DoesNotExist):
            return Response({'message': 'Nursery, Parent, or Request not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_nursery_join(request):
    if request.user.user_type != 'parent':
        return Response({
            'error': 'Only parents can request to join a nursery',
            'code': 'NOT_PARENT'
        }, status=status.HTTP_403_FORBIDDEN)

    nursery_id = request.data.get('nursery_id')
    try:
        nursery = Nursery.objects.get(id=nursery_id, status='accepted')
        parent = Parent.objects.get(admin=request.user)

        if NurseryParent.objects.filter(nursery=nursery, parent=parent).exists():
            return Response({
                'error': 'Request already sent',
                'code': 'DUPLICATE_REQUEST'
            }, status=status.HTTP_400_BAD_REQUEST)

        NurseryParent.objects.create(nursery=nursery, parent=parent, status='pending')

        create_notification(
            nursery,
            title="New Parent Join Request",
            message=f"Parent {parent.father_mother_name} has requested to join your nursery.",
            is_nursery=True
        )

        return Response({'success': True, 'message': 'Join request sent to nursery'}, status=status.HTTP_201_CREATED)
    except Nursery.DoesNotExist:
        return Response({
            'error': 'Nursery not found or not accepted',
            'code': 'NURSERY_NOT_FOUND'
        }, status=status.HTTP_404_NOT_FOUND)
    except Parent.DoesNotExist:
        return Response({
            'error': 'Parent not found',
            'code': 'PARENT_NOT_FOUND'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_child_profile(request):
    try:
        parent = Parent.objects.get(admin=request.user)
        children = Child.objects.filter(parent=parent)
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Parent.DoesNotExist:
        return Response({
            'error': 'Parent not found',
            'code': 'PARENT_NOT_FOUND'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_child(request):
    if request.user.user_type != 'parent':
        return Response({'error': 'Only parents can add children', 'code': 'NOT_PARENT'}, status=status.HTTP_403_FORBIDDEN)
    
    parent = Parent.objects.get(admin=request.user)
    child_data = {
        'parent': parent.id,
        'first_name': request.data.get('first_name'),
        'family_name': request.data.get('family_name'),
        'religion': request.data.get('religion', ''),
        'gender': request.data.get('gender'),
        'address': request.data.get('address', 'Unknown'),
        'date_of_birth': request.data.get('date_of_birth'),
        'phone': request.data.get('phone', ''),
        'guardian_job': request.data.get('guardian_job', 'Unknown')
    }
    serializer = ChildSerializer(data=child_data)
    if serializer.is_valid():
        child = serializer.save()
        return Response({'success': True, 'child_id': child.id}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid child data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nursery_details(request, nursery_id):
    try:
        nursery = Nursery.objects.get(id=nursery_id, status='accepted')
        serializer = NurserySerializer(nursery)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Nursery.DoesNotExist:
        return Response({'error': 'Nursery not found', 'code': 'NURSERY_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nursery_info(request):
    if request.user.user_type != 'nursery':
        return Response({'error': 'Only nurseries can access this', 'code': 'NOT_NURSERY'}, status=status.HTTP_403_FORBIDDEN)
    
    nursery = Nursery.objects.get(admin=request.user)
    serializer = NurserySerializer(nursery)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_nursery_info(request):
    if request.user.user_type != 'nursery':
        return Response({'error': 'Only nurseries can update this', 'code': 'NOT_NURSERY'}, status=status.HTTP_403_FORBIDDEN)
    
    nursery = Nursery.objects.get(admin=request.user)
    serializer = NurserySerializer(nursery, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Nursery updated'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    if request.user.user_type != 'nursery':
        return Response({'error': 'Only nurseries can access this', 'code': 'NOT_NURSERY'}, status=status.HTTP_403_FORBIDDEN)
    
    nursery = Nursery.objects.get(admin=request.user)
    requests = NurseryParent.objects.filter(nursery=nursery)
    serializer = ParentSerializer([req.parent for req in requests], many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_action(request):
    if request.user.user_type != 'nursery':
        return Response({'error': 'Only nurseries can access this', 'code': 'NOT_NURSERY'}, status=status.HTTP_403_FORBIDDEN)
    
    nursery = Nursery.objects.get(admin=request.user)
    parent_id = request.data.get('parent_id')
    action = request.data.get('action')
    
    try:
        parent = Parent.objects.get(id=parent_id)
        request_obj = NurseryParent.objects.get(nursery=nursery, parent=parent)
        if action == 'accept':
            request_obj.status = 'accepted'
            message = f"Your request to join {nursery.name} has been accepted."
        elif action == 'reject':
            request_obj.status = 'rejected'
            message = f"Your request to join {nursery.name} has been rejected."
        else:
            return Response({'error': 'Invalid action', 'code': 'INVALID_ACTION'}, status=status.HTTP_400_BAD_REQUEST)
        request_obj.save()
        create_notification(parent, title=f"Join Request {action.capitalize()}", message=message)
        return Response({'success': True, 'message': f'Parent request {action}ed'}, status=status.HTTP_200_OK)
    except (Parent.DoesNotExist, NurseryParent.DoesNotExist):
        return Response({'error': 'Parent or request not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_parent_requests(request):
    users_with_requests = User.objects.filter(
        parent_request__isnull=False, parent_request__ne='', user_type='parent'
    )
    parents = [Parent.objects.get(admin=user) for user in users_with_requests]
    serializer = ParentSerializer(parents, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_parent_request(request, parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        user = parent.admin  # تصحيح لـ admin_id
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)
        user.parent_request = f"Request for {parent.father_mother_name}"
        user.request_status = status
        user.save()
        create_notification(parent, title=f"Parent {status.capitalize()}", message=f"Your account has been {status} by the admin.")
        return Response({'success': True, 'message': f'Parent status updated to {status}'}, status=status.HTTP_200_OK)
    except Parent.DoesNotExist:
        return Response({'error': 'Parent not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_nursery_requests(request):
    users_with_requests = User.objects.filter(
        nursery_request__isnull=False, nursery_request__ne='', user_type='nursery'
    )
    nurseries = [Nursery.objects.get(admin=user) for user in users_with_requests]
    serializer = NurserySerializer(nurseries, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_nursery_request(request, nursery_id):
    try:
        nursery = Nursery.objects.get(id=nursery_id)
        user = nursery.admin  # تصحيح لـ admin_id
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)
        nursery.status = status
        nursery.save()
        user.nursery_request = f"Request for {nursery.name}"
        user.request_status = status
        user.save()
        create_notification(nursery, title=f"Nursery {status.capitalize()}", message=f"Your nursery {nursery.name} has been {status} by the admin.", is_nursery=True)
        return Response({'success': True, 'message': f'Nursery status updated to {status}'}, status=status.HTTP_200_OK)
    except Nursery.DoesNotExist:
        return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)