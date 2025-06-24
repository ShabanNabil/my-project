

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
import logging
import uuid
from .models import Child, Notification, Nursery, NurseryParent, Parent, User
from .serializers import ChildSerializer, NotificationSerializer, NurseryParentSerializer, NurserySerializer, ParentSerializer, UserSerializer

logger = logging.getLogger(__name__)

def create_notification(recipient, title, message, is_nursery=False):
    kwargs = {'is_read': False, 'title': title, 'message': message}
    if is_nursery:
        kwargs['nursery'] = recipient
    elif hasattr(recipient, 'user_type') and recipient.user_type == 'admin':
        kwargs['user'] = recipient
    else:
        kwargs['parent'] = recipient
    Notification.objects.create(**kwargs)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(nursery__admin_id=user).order_by('-id')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class ParentSignUpView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        user_data = {
            'full_name': request.data.get('full_name'),
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

            user = user_serializer.save()
            parent_data = {
                'admin_id': user,
                'full_name': request.data.get('full_name', ''),
                'address': request.data.get('address', 'Unknown'),
                'phone_number': request.data.get('phone_number', ''),
                'job': request.data.get('job', '')
            }
            if not parent_data['phone_number']:
                user.delete()
                return Response({
                    'error': 'Phone number is required',
                    'code': 'MISSING_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Parent.objects.filter(phone_number=parent_data['phone_number']).exists():
                user.delete()
                return Response({
                    'error': 'Phone number already exists',
                    'code': 'DUPLICATE_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)

            parent = Parent.objects.create(**parent_data)

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
logger = logging.getLogger(__name__)
@csrf_exempt
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

    logger.info(f"Login attempt for email: {email}")  # Add logging

    try:
        user = authenticate(request, email=email, password=password)
        if user is None:
            logger.warning(f"Authentication failed for email: {email}")
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        logger.info(f"Login successful for email: {email}")
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'user_type': 'parent',
            'message': 'Login successful for parent'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        logger.error(f"User not found for email: {email}")
        return Response({
            'error': 'Invalid credentials or not a parent',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)


class NurserySignUpView(APIView):
    permission_classes = [AllowAny]
    @csrf_exempt
    @transaction.atomic
    def post(self, request):
        full_name = request.data.get('full_name')
        if not full_name:
            return Response({
                'error': 'Full name is required',
                'code': 'MISSING_FULL_NAME'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'full_name': full_name,
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
                'phone_number': user_data.get('phone_number'),
                'address': request.data.get('location', 'Unknown'),
                'description': request.data.get('description', ''),
                'longitude': request.data.get('longitude', 0.0),
                'latitude': request.data.get('latitude', 0.0),
                'image': request.data.get('image', None)
            }
            if not nursery_data['phone_number']:
                user.delete()
                return Response({
                    'error': 'Phone number is required',
                    'code': 'MISSING_PHONE'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Nursery.objects.filter(phone_number=nursery_data['phone_number']).exists():
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
            user.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'nursery_id': nursery.admin_id.id,
                'nursery_status': 'active',
                'user_type': 'nursery',
                'redirect': '/nursery-information/'
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

@csrf_exempt
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
        if not check_password(password, user.password):
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        redirect_url = '/nursery-information/' if nursery.status == 'pending' else None
        response_data = {
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'nursery_id': nursery.admin_id.id,
            'nursery_status': nursery.status,
            'user_type': 'nursery',
            'message': 'Login successful for nursery',
            'redirect': redirect_url
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except (User.DoesNotExist, Nursery.DoesNotExist):
        return Response({
            'error': 'Invalid credentials or not a nursery',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    logger.info(f"Received admin login request: {request.data}")
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error': 'Email and password are required',
            'code': 'MISSING_CREDENTIALS'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = authenticate(request, email=email, password=password)
        if user is None:
            logger.error(f"Authentication failed for email {email}")
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not (user.is_staff and user.is_superuser and user.user_type == 'admin'):
            logger.error(f"User {email} lacks admin privileges: is_staff={user.is_staff}, is_superuser={user.is_superuser}, user_type={user.user_type}")
            return Response({
                'error': 'User is not an admin',
                'code': 'NOT_ADMIN'
            }, status=status.HTTP_400_BAD_REQUEST)

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
    except Exception as e:
        logger.error(f"Admin login error for email {email}: {str(e)}")
        return Response({
            'error': 'Invalid credentials or not an admin',
            'code': 'INVALID_CREDENTIALS'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nurseries(request):
    query = request.query_params.get('q', '')
    nurseries = Nursery.objects.filter(status='accepted')
    if query:
        nurseries = nurseries.filter(
            Q(name__icontains=query) | Q(address__icontains=query)
        )
    serializer = NurserySerializer(nurseries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
        if status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

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
        if status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        nursery.status = status
        nursery.save()

        create_notification(
            nursery,
            title=f"Nursery {status.capitalize()}",
            message=f"Your nursery {nursery.name} has been {status} by the admin.",
            is_nursery=True
        )

        return Response({'success': True, 'message': f'Nursery status updated to {status}'}, status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)

def create_notification(nursery, title, message, is_nursery=True):
    # افترض إن الدالة دي موجودة وبتعمل إشعار
    pass

clogger = logging.getLogger(__name__)

def create_notification(nursery, title, message, is_nursery=True):
    # افترض إن الدالة دي موجودة وبتعمل إشعار
    pass
#داش الادمن الخاص بالحضانات 
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        """جلب الحضانات المعلقة"""
        try:
            nurseries = Nursery.objects.filter(status='pending')
            serializer = NurserySerializer(nurseries, many=True)
            logger.info(f"Found {len(serializer.data)} pending nurseries")
            return Response({
                'pending_nurseries': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in AdminDashboardView.get: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """قبول أو رفض حضانة"""
        nursery_id = kwargs.get('nursery_id')
        if not nursery_id:
            logger.error("Missing nursery_id in URL")
            return Response({'error': 'Missing nursery_id'}, status=status.HTTP_400_BAD_REQUEST)

        status_value = request.data.get('status')
        if status_value not in ['accepted', 'rejected']:
            logger.error(f"Invalid status: {status_value}")
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # استخدم admin_id بدل id
            nursery = Nursery.objects.get(admin_id=nursery_id)
            nursery.status = status_value
            nursery.save()
            create_notification(
                nursery,
                title=f"Nursery {status_value.capitalize()}",
                message=f"Your nursery {nursery.name} has been {status_value} by the admin.",
                is_nursery=True
            )
            logger.info(f"Nursery {nursery_id} status updated to {status_value} by {request.user.email}")
            return Response({
                'success': True,
                'message': f'Nursery status updated to {status_value}'
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminDashboardView.post: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        """تعديل بيانات الحضانة"""
        nursery_id = kwargs.get('nursery_id')
        if not nursery_id:
            logger.error("Missing nursery_id in URL")
            return Response({'error': 'Missing nursery_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery = Nursery.objects.get(admin_id=nursery_id)
            serializer = NurserySerializer(nursery, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Nursery {nursery_id} updated by {request.user.email}")
                return Response({
                    'success': True,
                    'message': f'Nursery {nursery_id} updated',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"Invalid data for nursery {nursery_id}: {serializer.errors}")
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminDashboardView.put: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """حذف حضانة"""
        nursery_id = kwargs.get('nursery_id')
        if not nursery_id:
            logger.error("Missing nursery_id in URL")
            return Response({'error': 'Missing nursery_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery = Nursery.objects.get(admin_id=nursery_id)
            nursery_name = nursery.name
            nursery.delete()
            logger.info(f"Nursery {nursery_id} ({nursery_name}) deleted by {request.user.email}")
            return Response({
                'success': True,
                'message': f'Nursery {nursery_name} deleted'
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminDashboardView.delete: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        if status not in ['accepted', 'rejected']:
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

class NurseryDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nursery_id: int):
        try:
            nursery = Nursery.objects.get(admin_id=nursery_id)
            if nursery.admin_id != request.user and not request.user.is_superuser:
                return Response({'message': 'Unauthorized', 'code': 'UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)

            status_filter = request.query_params.get('status', None)
            requests = NurseryParent.objects.filter(nursery=nursery)
            if status_filter:
                requests = requests.filter(status=status_filter)

            if not requests.exists():
                return Response({
                    'nursery': NurserySerializer(nursery).data,
                    'requests': [],
                    'message': 'No requests found'
                }, status=status.HTTP_200_OK)

            serializer = NurseryParentSerializer(requests, many=True)
            return Response({
                'nursery': NurserySerializer(nursery).data,
                'requests': serializer.data
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            return Response({'message': 'Nursery not found or you do not have access', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, nursery_id: int):
        try:
            nursery = Nursery.objects.get(admin_id=nursery_id)
            if nursery.admin_id != request.user and not request.user.is_superuser:
                return Response({'message': 'Unauthorized', 'code': 'UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)

            parent_id = request.data.get('parent_id')
            action = request.data.get('action')

            if not parent_id or not action:
                return Response({'message': 'Missing parent_id or action', 'code': 'MISSING_DATA'}, status=status.HTTP_400_BAD_REQUEST)

            parent = Parent.objects.get(id=parent_id)
            request_obj = NurseryParent.objects.get(nursery=nursery, parent=parent)

            if action not in ['accept', 'reject']:
                return Response({'message': 'Invalid action', 'code': 'INVALID_ACTION'}, status=status.HTTP_400_BAD_REQUEST)

            if action == 'accept':
                request_obj.status = 'accepted'
                message = f"Your request to join {nursery.name} for child {request_obj.child.child_name} has been accepted."
            elif action == 'reject':
                request_obj.status = 'rejected'
                message = f"Your request to join {nursery.name} for child {request_obj.child.child_name} has been rejected."

            request_obj.save()
            create_notification(
                parent,
                title=f"Join Request {action.capitalize()}",
                message=message
            )
            return Response({'message': f'Parent request {action}ed', 'request_status': request_obj.status}, status=status.HTTP_200_OK)
        except (Nursery.DoesNotExist, Parent.DoesNotExist, NurseryParent.DoesNotExist):
            return Response({'message': 'Nursery, Parent, or Request not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

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
    logger.info(f"Add child request received: {request.data}")
    if hasattr(request.user, 'user_type') and request.user.user_type != 'parent':
        logger.error(f"User {request.user.email} is not a parent")
        return Response({'error': 'Only parents can add children', 'code': 'NOT_PARENT'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        parent, created = Parent.objects.get_or_create(admin_id=request.user, defaults={
            'full_name': request.user.first_name or request.user.email.split('@')[0],
            'phone_number': request.data.get('phone_number', '')
        })
    except Parent.MultipleObjectsReturned:
        parent = Parent.objects.filter(admin_id=request.user).first()

    child_data = {
        'parent': parent.id,
        'child_name': request.data.get('child_name'),
        'date_of_birth': request.data.get('date_of_birth'),
        'father_mother_name': request.data.get('father_mother_name'),
        'job': request.data.get('job', ''),
        'address': request.data.get('address', 'Unknown'),
        'phone_number': request.data.get('phone_number', ''),
        'another_phone_number': request.data.get('another_phone_number', ''),
        'gender': request.data.get('gender', '')
    }

    required_fields = ['child_name', 'date_of_birth', 'father_mother_name', 'phone_number']
    missing_fields = [field for field in required_fields if not child_data[field]]
    if missing_fields:
        logger.error(f"Missing fields: {missing_fields}")
        return Response({
            'error': f'Missing required fields: {", ".join(missing_fields)}',
            'code': 'MISSING_FIELDS'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if child_data['gender'] and child_data['gender'] not in ['male', 'female']:
        logger.error(f"Invalid gender: {child_data['gender']}")
        return Response({
            'error': 'Gender must be "male" or "female"',
            'code': 'INVALID_GENDER'
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = ChildSerializer(data=child_data)
    if serializer.is_valid():
        child = serializer.save()
        nursery_id = request.data.get('nursery_id')
        if nursery_id:
            try:
                nursery = Nursery.objects.get(admin_id__id=nursery_id)
                NurseryParent.objects.update_or_create(
                    nursery=nursery,
                    parent=parent,
                    child=child,
                    defaults={'status': 'pending'}
                )
                logger.info(f"Request sent to nursery {nursery.name}")
                return Response({
                    'success': True,
                    'child_id': child.id,
                    'message': f'Request sent to nursery {nursery.name}'
                }, status=status.HTTP_201_CREATED)
            except Nursery.DoesNotExist:
                logger.error(f"Nursery with ID {nursery_id} not found")
                return Response({
                    'error': 'Nursery not found',
                    'code': 'NOT_FOUND'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'child_id': child.id}, status=status.HTTP_201_CREATED)
    logger.error(f"Serializer errors: {serializer.errors}")
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
    logger.info(f"User: {request.user}, is_staff: {request.user.is_staff}, is_superuser: {request.user.is_superuser}, user_type: {request.user.user_type}")
    
    try:
        users_with_requests = User.objects.filter(
            parent_request__isnull=False,
            parent_request__gt='',
            user_type='parent'
        )
        parents = []
        for user in users_with_requests:
            try:
                parent = Parent.objects.get(admin_id=user)
                parents.append(parent)
            except Parent.DoesNotExist:
                logger.error(f"No Parent found for user: {user.id}")
                continue
        
        logger.info(f"Found {len(parents)} parent requests")
        serializer = ParentSerializer(parents, many=True)
        return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error in get_parent_requests: {str(e)}")
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_nursery_requests(request):
    logger.info(f"User: {request.user}, is_staff: {request.user.is_staff}, is_superuser: {request.user.is_superuser}, user_type: {request.user.user_type}")
    try:
        users_with_requests = User.objects.filter(
            nursery_request__isnull=False,
            nursery_request__gt='',
            user_type='nursery'
        )
        nurseries = []
        for user in users_with_requests:
            try:
                nursery = Nursery.objects.get(admin_id=user)
                nurseries.append(nursery)
            except Nursery.DoesNotExist:
                logger.error(f"No Nursery found for user: {user.id}")
                continue
        
        logger.info(f"Found {len(nurseries)} nursery requests")
        serializer = NurserySerializer(nurseries, many=True)
        return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_nursery_requests: {str(e)}")
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_parent_request(request, parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        user = parent.admin
        status = request.data.get('status')
        if status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)
        user.parent_request = f"Request for {parent.father_mother_name}"
        user.request_status = status
        user.save()
        create_notification(parent, title=f"Parent {status.capitalize()}", message=f"Your account has been {status} by the admin.")
        return Response({'success': True, 'message': f'Parent status updated to {status}'}, status=status.HTTP_200_OK)
    except Parent.DoesNotExist:
        return Response({'error': 'Parent not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_approve_nursery(request, nursery_id):
    try:
        nursery = Nursery.objects.get(id=nursery_id)
        status = request.data.get('status')
        if status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        nursery.status = status
        nursery.save()
        create_notification(
            nursery,
            title=f"Nursery {status.capitalize()}",
            message=f"Your nursery {nursery.name} has been {status} by the admin.",
            is_nursery=True
        )
        return Response({'success': True, 'message': f'Nursery status updated to {status}'}, status=status.HTTP_200_OK)
    except Nursery.DoesNotExist:
        return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_nursery_request(request, nursery_id):
    try:
        nursery = Nursery.objects.get(id=nursery_id)
        user = nursery.admin
        status = request.data.get('status')
        if status not in ['accepted', 'rejected']:
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

logger = logging.getLogger(__name__)
#داش بورد الادمن لاولياء الامور 
class AdminParentDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """جلب الطلبات المعلقة"""
        try:
            nursery_id = request.query_params.get('nursery_id')
            queryset = NurseryParent.objects.filter(status='pending')
            if nursery_id:
                queryset = queryset.filter(nursery_id=nursery_id)
            # لو المستخدم حضانة، جيب طلباته بس
            if request.user.user_type == 'nursery':
                nursery = Nursery.objects.get(admin_id=request.user)
                queryset = queryset.filter(nursery=nursery)
            serializer = NurseryParentSerializer(queryset, many=True)
            logger.info(f"Found {len(serializer.data)} pending parent requests")
            return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery not found for user {request.user.email}")
            return Response({'error': 'Nursery not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminParentDashboard.get: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """قبول أو رفض طلب"""
        if not (request.user.is_staff or request.user.user_type == 'nursery'):
            logger.error(f"User {request.user.email} not authorized")
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')
        child_id = request.data.get('child_id')
        parent_id = request.data.get('parent_id')
        nursery_id = request.data.get('nursery_id')

        if not all([action, child_id, parent_id, nursery_id]):
            logger.error(f"Missing fields in request: {request.data}")
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery_parent = NurseryParent.objects.get(
                child_id=child_id,
                parent_id=parent_id,
                nursery_id=nursery_id,
                status='pending'
            )
            # لو المستخدم حضانة، تأكد إن الطلب بتاعه
            if request.user.user_type == 'nursery':
                nursery = Nursery.objects.get(admin_id=request.user)
                if nursery_parent.nursery != nursery:
                    return Response({'error': 'Not authorized for this nursery'}, status=status.HTTP_403_FORBIDDEN)

            if action == 'accept':
                nursery_parent.status = 'accepted'
                nursery_parent.save()
                logger.info(f"Child {child_id} accepted for nursery {nursery_id} by {request.user.email}")
                return Response({'success': True, 'message': f'Child {child_id} accepted'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                nursery_parent.status = 'rejected'
                nursery_parent.save()
                logger.info(f"Child {child_id} rejected for nursery {nursery_id} by {request.user.email}")
                return Response({'success': True, 'message': f'Child {child_id} rejected'}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Invalid action: {action}")
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except NurseryParent.DoesNotExist:
            logger.error(f"No pending request found for child {child_id}")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminParentDashboard.post: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """تعديل بيانات طلب، والد، أو طفل"""
        if not request.user.is_staff:  # بس الـ admin يقدر يعدل
            logger.error(f"User {request.user.email} not authorized")
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        child_id = request.data.get('child_id')
        parent_id = request.data.get('parent_id')
        nursery_id = request.data.get('nursery_id')

        if not all([child_id, parent_id, nursery_id]):
            logger.error(f"Missing fields in request: {request.data}")
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery_parent = NurseryParent.objects.get(
                child_id=child_id,
                parent_id=parent_id,
                nursery_id=nursery_id
            )
            # تعديل بيانات الوالد
            parent_data = request.data.get('parent', {})
            if parent_data:
                parent = nursery_parent.parent
                parent_serializer = ParentSerializer(parent, data=parent_data, partial=True)
                if parent_serializer.is_valid():
                    parent_serializer.save()
                else:
                    return Response({'error': parent_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # تعديل بيانات الطفل
            child_data = request.data.get('child', {})
            if child_data:
                child = nursery_parent.child
                child_serializer = ChildSerializer(child, data=child_data, partial=True)
                if child_serializer.is_valid():
                    child_serializer.save()
                else:
                    return Response({'error': child_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Updated data for child {child_id} in nursery {nursery_id} by {request.user.email}")
            return Response({'success': True, 'message': f'Data updated for child {child_id}'}, status=status.HTTP_200_OK)
        except NurseryParent.DoesNotExist:
            logger.error(f"No request found for child {child_id}")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminParentDashboard.put: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """حذف طلب"""
        if not request.user.is_staff:  # بس الـ admin يقدر يحذف
            logger.error(f"User {request.user.email} not authorized")
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        nursery_parent_id = request.data.get('nursery_parent_id')
        if not nursery_parent_id:
            logger.error(f"Missing nursery_parent_id in request")
            return Response({'error': 'Missing nursery_parent_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery_parent = NurseryParent.objects.get(id=nursery_parent_id)
            nursery_parent.delete()
            logger.info(f"NurseryParent {nursery_parent_id} deleted by {request.user.email}")
            return Response({'success': True, 'message': f'Request {nursery_parent_id} deleted'}, status=status.HTTP_200_OK)
        except NurseryParent.DoesNotExist:
            logger.error(f"NurseryParent {nursery_parent_id} not found")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AdminParentDashboard.delete: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AdminNurseryDashboard(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, nursery_id=None):
        if nursery_id:
            try:
                nursery = Nursery.objects.get(admin_id=nursery_id)
                serializer = NurserySerializer(nursery)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Nursery.DoesNotExist:
                return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        else:
            nurseries = Nursery.objects.filter(status='pending')
            serializer = NurserySerializer(nurseries, many=True)
            return Response({
                'pending_nurseries': serializer.data
            }, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, nursery_id=None):
        if not nursery_id:
            return Response({'error': 'Nursery ID is required', 'code': 'MISSING_NURSERY_ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery = Nursery.objects.get(admin_id=nursery_id)
            requested_status = request.data.get('status')
            if requested_status not in ['accepted', 'rejected']:
                return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

            nursery.status = requested_status
            nursery.save()
            create_notification(
                nursery,
                title=f"Nursery {requested_status.capitalize()}",
                message=f"Your nursery {nursery.name} has been {requested_status} by the admin.",
                is_nursery=True
            )
            return Response({'success': True, 'message': f'Nursery status updated to {requested_status}'}, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            return Response({'error': 'Nursery not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

class NurserySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('q', None)
        if search_query:
            nurseries = Nursery.objects.filter(status='accepted', name__icontains=search_query)
        else:
            nurseries = Nursery.objects.filter(status='accepted')
        serializer = NurserySerializer(nurseries, many=True)
        return Response(serializer.data)

class NurseryInformationView(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @transaction.atomic
    def post(self, request):
        user = request.user
        if user.user_type != 'nursery':
            return Response({
                'error': 'Only nurseries can submit information',
                'code': 'UNAUTHORIZED'
            }, status=403)

        try:
            nursery = Nursery.objects.get(admin_id=user)
        except Nursery.DoesNotExist:
            return Response({
                'error': 'Nursery not found',
                'code': 'NOT_FOUND'
            }, status=404)

        data = {
            'name': request.data.get('name', nursery.name),
            'phone_number': request.data.get('phone', nursery.phone_number),
            'address': request.data.get('location', nursery.address),
            'description': request.data.get('description', nursery.description),
            'longitude': request.data.get('longitude', nursery.longitude),
            'latitude': request.data.get('latitude', nursery.latitude),
            'status': 'pending',
        }

        if 'photo' in request.FILES:
            data['image'] = request.FILES['photo']
        elif 'photo' not in request.data:
            data['image'] = nursery.image if nursery.image else None
        else:
            data['image'] = None

        serializer = NurserySerializer(nursery, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            admin_users = User.objects.filter(user_type='admin')
            for admin in admin_users:
                create_notification(
                    admin,
                    title="New Nursery Information Request",
                    message=f"Nursery {nursery.name} submitted information for approval.",
                    is_nursery=False
                )
            return Response({
                'success': True,
                'message': 'Information submitted for approval',
                'nursery_status': 'pending'
            }, status=200)
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=400)

    def get(self, request):
        user = request.user
        if user.user_type != 'nursery':
            return Response({
                'error': 'Only nurseries can access this page',
                'code': 'UNAUTHORIZED'
            }, status=403)

        try:
            nursery = Nursery.objects.get(admin_id=user)
            if nursery.status != 'accepted':
                return Response({
                    'error': 'Nursery not approved yet',
                    'code': 'NOT_APPROVED'
                }, status=403)

            notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
            menu = [
                {'name': 'Home', 'url': '/nursery-information/', 'icon': 'home'},
                {'name': 'Edit', 'url': '/nursery-edit/', 'icon': 'edit'},
                {'name': 'Dashboard', 'url': f'/nursery-dashboard/{nursery.admin_id.id}/', 'icon': 'dashboard'}
            ]
            response_data = {
                'success': True,
                'nursery_data': {
                    'name': nursery.name,
                    'address': nursery.address,
                    'phone_number': nursery.phone_number,
                    'status': nursery.status
                },
                'notifications': NotificationSerializer(notifications, many=True).data,
                'menu': menu
            }
            return Response(response_data, status=200)
        except Nursery.DoesNotExist:
            return Response({
                'error': 'Nursery not found',
                'code': 'NOT_FOUND'
            }, status=404)

class NurseryHomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'nursery':
            return Response({
                'error': 'Only nurseries can access this',
                'code': 'UNAUTHORIZED'
            }, status=status.HTTP_403_FORBIDDEN)

        nursery = Nursery.objects.get(admin_id=user)
        if nursery.status != 'approved':
            return Response({
                'error': 'Your nursery is not approved yet',
                'code': 'UNAUTHORIZED'
            }, status=status.HTTP_403_FORBIDDEN)

        notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
        notification_serializer = NotificationSerializer(notifications, many=True)

        return Response({
            'success': True,
            'nursery_data': NurserySerializer(nursery).data,
            'notifications': notification_serializer.data,
            'menu': [
                {'title': 'Dashboard', 'url': '/nursery-dashboard/'},
                {'title': 'Edit Information', 'url': '/nursery-edit/'}
            ]
        }, status=status.HTTP_200_OK)

class NurseryEditView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        if user.user_type != 'nursery':
            return Response({
                'error': 'Only nurseries can edit information',
                'code': 'UNAUTHORIZED'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            nursery = Nursery.objects.get(admin_id=user)
            if nursery.status != 'approved':
                return Response({
                    'error': 'Your nursery is not approved yet',
                    'code': 'UNAUTHORIZED'
                }, status=status.HTTP_403_FORBIDDEN)

            data = {
                'name': request.data.get('name', nursery.name),
                'phone_number': request.data.get('phone', nursery.phone_number),
                'capacity': request.data.get('capacity', nursery.capacity),
                'address': request.data.get('location', nursery.address),
                'description': request.data.get('description', nursery.description),
                'longitude': request.data.get('longitude', nursery.longitude),
                'latitude': request.data.get('latitude', nursery.latitude),
                'image': request.data.get('photo', nursery.image),
            }
            serializer = NurserySerializer(nursery, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Information updated successfully',
                    'nursery_status': nursery.status
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Invalid data',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Nursery.DoesNotExist:
            return Response({
                'error': 'Nursery not found',
                'code': 'NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)
logger = logging.getLogger(__name__)

def create_notification(recipient, title, message, is_nursery=False):
    # Placeholder for notification logic
    pass

class NurseryParentDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nursery_id, *args, **kwargs):
        """جلب طلبات الآباء المعلقة للحضانة"""
        try:
            # جلب الحضانة بناءً على admin_id
            nursery = Nursery.objects.get(admin_id=nursery_id)
            # التأكد إن المستخدم هو صاحب الحضانة
            if nursery.admin_id != request.user or request.user.user_type != 'nursery':
                logger.error(f"User {request.user.email} not authorized for nursery {nursery_id}")
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            # جلب الطلبات المعلقة
            queryset = NurseryParent.objects.filter(nursery=nursery, status='pending')
            serializer = NurseryParentSerializer(queryset, many=True)
            logger.info(f"Found {len(serializer.data)} pending parent requests for nursery {nursery_id}")
            return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in NurseryParentDashboard.get: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request, nursery_id, *args, **kwargs):
        """قبول أو رفض طلب والد"""
        try:
            # جلب الحضانة بناءً على admin_id
            nursery = Nursery.objects.get(admin_id=nursery_id)
            # التأكد إن المستخدم هو صاحب الحضانة
            if nursery.admin_id != request.user or request.user.user_type != 'nursery':
                logger.error(f"User {request.user.email} not authorized for nursery {nursery_id}")
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            child_id = request.data.get('child_id')
            parent_id = request.data.get('parent_id')
            action = request.data.get('action')

            if not all([child_id, parent_id, action]):
                logger.error(f"Missing fields in request: {request.data}")
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            if action not in ['accept', 'reject']:
                logger.error(f"Invalid action: {action}")
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            nursery_parent = NurseryParent.objects.get(
                child_id=child_id,
                parent_id=parent_id,
                nursery=nursery,
                status='pending'
            )

            nursery_parent.status = 'accepted' if action == 'accept' else 'rejected'
            nursery_parent.save()

            # إشعار للوالد
            parent = nursery_parent.parent
            create_notification(
                recipient=parent,
                title=f"Child Request {action.capitalize()}ed",
                message=f"Your request for {nursery_parent.child.child_name} to join {nursery.name} has been {action}ed.",
                is_nursery=False
            )

            logger.info(f"Child {child_id} {action}ed for nursery {nursery_id} by {request.user.email}")
            return Response({
                'success': True,
                'message': f'Child {child_id} {action}ed'
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        except NurseryParent.DoesNotExist:
            logger.error(f"No pending request found for child {child_id}")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in NurseryParentDashboard.post: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def put(self, request, nursery_id, *args, **kwargs):
        """تعديل بيانات الوالد أو الطفل"""
        try:
            # جلب الحضانة بناءً على admin_id
            nursery = Nursery.objects.get(admin_id=nursery_id)
            # التأكد إن المستخدم هو صاحب الحضانة
            if nursery.admin_id != request.user or request.user.user_type != 'nursery':
                logger.error(f"User {request.user.email} not authorized for nursery {nursery_id}")
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            child_id = request.data.get('child_id')
            parent_id = request.data.get('parent_id')

            if not all([child_id, parent_id]):
                logger.error(f"Missing child_id or parent_id in request: {request.data}")
                return Response({'error': 'Missing child_id or parent_id'}, status=status.HTTP_400_BAD_REQUEST)

            nursery_parent = NurseryParent.objects.get(
                child_id=child_id,
                parent_id=parent_id,
                nursery=nursery
            )

            # تعديل بيانات الوالد
            parent_data = request.data.get('parent', {})
            if parent_data:
                parent = nursery_parent.parent
                parent_serializer = ParentSerializer(parent, data=parent_data, partial=True)
                if parent_serializer.is_valid():
                    parent_serializer.save()
                else:
                    logger.error(f"Invalid parent data: {parent_serializer.errors}")
                    return Response({'error': parent_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # تعديل بيانات الطفل
            child_data = request.data.get('child', {})
            if child_data:
                child = nursery_parent.child
                child_serializer = ChildSerializer(child, data=child_data, partial=True)
                if child_serializer.is_valid():
                    child_serializer.save()
                else:
                    logger.error(f"Invalid child data: {child_serializer.errors}")
                    return Response({'error': child_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Updated data for child {child_id} in nursery {nursery_id} by {request.user.email}")
            return Response({
                'success': True,
                'message': f'Data updated for child {child_id}'
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        except NurseryParent.DoesNotExist:
            logger.error(f"No request found for child {child_id}")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in NurseryParentDashboard.put: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request, nursery_id, *args, **kwargs):
        """حذف طلب والد"""
        try:
            # جلب الحضانة بناءً على admin_id
            nursery = Nursery.objects.get(admin_id=nursery_id)
            # التأكد إن المستخدم هو صاحب الحضانة
            if nursery.admin_id != request.user or request.user.user_type != 'nursery':
                logger.error(f"User {request.user.email} not authorized for nursery {nursery_id}")
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            child_id = request.data.get('child_id')
            parent_id = request.data.get('parent_id')

            if not all([child_id, parent_id]):
                logger.error(f"Missing child_id or parent_id in request: {request.data}")
                return Response({'error': 'Missing child_id or parent_id'}, status=status.HTTP_400_BAD_REQUEST)

            nursery_parent = NurseryParent.objects.get(
                child_id=child_id,
                parent_id=parent_id,
                nursery=nursery
            )

            nursery_parent_id = nursery_parent.id
            nursery_parent.delete()

            logger.info(f"NurseryParent {nursery_parent_id} deleted by {request.user.email}")
            return Response({
                'success': True,
                'message': f'Request {nursery_parent_id} deleted'
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            logger.error(f"Nursery with admin_id {nursery_id} not found")
            return Response({'error': 'Nursery not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        except NurseryParent.DoesNotExist:
            logger.error(f"No request found for child {child_id}")
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in NurseryParentDashboard.delete: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)