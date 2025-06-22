

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
from .serializers import UserSerializer, NurserySerializer, ParentSerializer, ChildSerializer, NotificationSerializer, NurseryParentSerializer
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.db import transaction, models
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action
from django.db.models import Q

def create_notification(recipient, title, message, is_nursery=False):
    kwargs = {'is_read': False, 'title': title, 'message': message}
    if is_nursery:
        kwargs['nursery'] = recipient
    elif hasattr(recipient, 'user_type') and recipient.user_type == 'admin':
        kwargs['user'] = recipient  # للأدمنز
    else:
        kwargs['parent'] = recipient  # للوالدين
    Notification.objects.create(**kwargs)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # جلب الإشعارات المرتبطة بالـ User الحالي (حضانة)
        user = request.user
        notifications = Notification.objects.filter(nursery__admin_id=user).order_by('-id')  # الأحدث أولاً
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

# ============ تمام شغال =====================================
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
#  ==================================================================
# ==================================تماممممممممم=========================
import logging

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

# شغال تمام ===========================================================
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
                # نزلنا status = 'pending'
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
                'nursery_status': 'active',  # بدل pending
                'user_type': 'nursery',
                'redirect': '/nursery-information/'  # تحويلة لصفحة التسجيل
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
# ==================================================================

# ===================== شغال تمام ======================================
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
# =================================================================

logger = logging.getLogger(__name__)
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
        # التحقق من الـ authentication أولاً
        user = authenticate(request, email=email, password=password)
        if user is None:
            logger.error(f"Authentication failed for email {email}")
            return Response({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # التحقق من إن المستخدم admin
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
# ======================================================================
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
        if status not in ['accepted', 'rejected']:  # نزلنا pending
            return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

        create_notification(
            parent,
            title=f"Parent {status.capitalize()}",
            message=f"Your account has been {status} by the admin."
        )

        return Response({'success': True, 'message': f'Parent status updated to {status}'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not (request.user.is_staff and request.user.is_superuser):  # تعديل هنا
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
        if status not in ['accepted', 'rejected']:  # نزلنا pending
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
    

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        nurseries = Nursery.objects.filter(status='pending')
        serializer = NurserySerializer(nurseries, many=True)
        return Response({
            'pending_nurseries': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, nursery_id):
        try:
            # استخدام admin_id بدل id لأن ده الـ primary key بتاع Nursery
            nursery = Nursery.objects.get(admin_id=nursery_id)
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
        except Exception as e:
            return Response({'error': str(e), 'code': 'SERVER_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        if status not in ['accepted', 'rejected']:  # نزلنا pending
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


# class NurseryDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, nursery_id: int):
#         try:
#             nursery = Nursery.objects.get(admin_id=nursery_id)
#             if nursery.admin != request.user and not request.user.is_superuser:
#                 return Response({'message': 'Unauthorized', 'code': 'UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)

#             status_filter = request.query_params.get('status', None)
#             requests = NurseryParent.objects.filter(nursery=nursery)
#             if status_filter:
#                 requests = requests.filter(status=status_filter)

#             if not requests.exists():
#                 return Response({
#                     'nursery': NurserySerializer(nursery).data,
#                     'requests': [],
#                     'message': 'No requests found'
#                 }, status=status.HTTP_200_OK)

#             serializer = NurseryParentSerializer(requests, many=True)
#             return Response({
#                 'nursery': NurserySerializer(nursery).data,
#                 'requests': serializer.data
#             }, status=status.HTTP_200_OK)
#         except Nursery.DoesNotExist:
#             return Response({'message': 'Nursery not found or you do not have access', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, nursery_id: int):
#         try:
#             nursery = Nursery.objects.get(admin_id=nursery_id)
#             if nursery.admin != request.user and not request.user.is_superuser:
#                 return Response({'message': 'Unauthorized', 'code': 'UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)

#             parent_id = request.data.get('parent_id')
#             action = request.data.get('action')

#             if not parent_id or not action:
#                 return Response({'message': 'Missing parent_id or action', 'code': 'MISSING_DATA'}, status=status.HTTP_400_BAD_REQUEST)

#             parent = Parent.objects.get(id=parent_id)
#             request_obj = NurseryParent.objects.get(nursery=nursery, parent=parent)

#             if action not in ['accept', 'reject']:
#                 return Response({'message': 'Invalid action', 'code': 'INVALID_ACTION'}, status=status.HTTP_400_BAD_REQUEST)

#             if action == 'accept':
#                 request_obj.status = 'accepted'
#                 message = f"Your request to join {nursery.name} for child {request_obj.child.child_name} has been accepted."
#             elif action == 'reject':
#                 request_obj.status = 'rejected'
#                 message = f"Your request to join {nursery.name} for child {request_obj.child.child_name} has been rejected."

#             request_obj.save()
#             create_notification(
#                 parent,
#                 title=f"Join Request {action.capitalize()}",
#                 message=message
#             )
#             return Response({'message': f'Parent request {action}ed', 'request_status': request_obj.status}, status=status.HTTP_200_OK)
#         except (Nursery.DoesNotExist, Parent.DoesNotExist, NurseryParent.DoesNotExist):
#             return Response({'message': 'Nursery, Parent, or Request not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_child(request):
#     if request.user.user_type != 'parent':
#         return Response({'error': 'Only parents can add children', 'code': 'NOT_PARENT'}, status=status.HTTP_403_FORBIDDEN)
    
#     parent = Parent.objects.get(admin_=request.user)
#     child_data = {
#         'parent': parent.id,
#         'child_name': request.data.get('child_name'),
#         'date_of_birth': request.data.get('date_of_birth'),
#         'father_mother_name': request.data.get('father_mother_name'),
#         'job': request.data.get('job', ''),
#         'address': request.data.get('address', 'Unknown'),
#         'phone_number': request.data.get('phone_number', ''),
#         'another_phone_number': request.data.get('another_phone_number', ''),
#         'gender': request.data.get('gender', '')
#     }
#     required_fields = ['child_name', 'date_of_birth', 'father_mother_name', 'phone_number']
#     missing_fields = [field for field in required_fields if not child_data[field]]
#     if missing_fields:
#         return Response({
#             'error': f'Missing required fields: {", ".join(missing_fields)}',
#             'code': 'MISSING_FIELDS'
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     if child_data['gender'] and child_data['gender'] not in ['male', 'female']:
#         return Response({
#             'error': 'Gender must be "male" or "female"',
#             'code': 'INVALID_GENDER'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     serializer = ChildSerializer(data=child_data)
#     if serializer.is_valid():
#         child = serializer.save()
#         nursery_id = request.data.get('nursery_id')
#         if nursery_id:
#             try:
#                 nursery = Nursery.objects.get(admin_id=nursery_id)
#                 NurseryParent.objects.update_or_create(
#                     nursery=nursery,
#                     parent=parent,
#                     child=child,
#                     defaults={'status': 'pending'}
#                 )
#                 return Response({
#                     'success': True,
#                     'child_id': child.id,
#                     'message': f'Request sent to nursery {nursery.name}'
#                 }, status=status.HTTP_201_CREATED)
#             except Nursery.DoesNotExist:
#                 return Response({
#                     'error': 'Nursery not found',
#                     'code': 'NOT_FOUND'
#                 }, status=status.HTTP_404_NOT_FOUND)
#         return Response({'success': True, 'child_id': child.id}, status=status.HTTP_201_CREATED)
#     return Response({'error': 'Invalid child data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_child(request):
    # التحقق من user_type
    if hasattr(request.user, 'user_type') and request.user.user_type != 'parent':
        return Response({'error': 'Only parents can add children', 'code': 'NOT_PARENT'}, status=status.HTTP_403_FORBIDDEN)
    
    # استخراج أو إنشاء الـ Parent باستخدام admin_id
    try:
        parent, created = Parent.objects.get_or_create(admin_id=request.user, defaults={
            'full_name': request.user.first_name or request.user.email.split('@')[0],
            'phone_number': request.data.get('phone_number', '')
        })
    except Parent.MultipleObjectsReturned:
        parent = Parent.objects.filter(admin_id=request.user).first()

    # تجميع بيانات الطفل
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

    # التحقق من الحقول المطلوبة
    required_fields = ['child_name', 'date_of_birth', 'father_mother_name', 'phone_number']
    missing_fields = [field for field in required_fields if not child_data[field]]
    if missing_fields:
        return Response({
            'error': f'Missing required fields: {", ".join(missing_fields)}',
            'code': 'MISSING_FIELDS'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # التحقق من الجنس
    if child_data['gender'] and child_data['gender'] not in ['male', 'female']:
        return Response({
            'error': 'Gender must be "male" or "female"',
            'code': 'INVALID_GENDER'
        }, status=status.HTTP_400_BAD_REQUEST)

    # تصنيف البيانات وتخزينها
    serializer = ChildSerializer(data=child_data)
    if serializer.is_valid():
        child = serializer.save()
        nursery_id = request.data.get('nursery_id')
        if nursery_id:
            try:
                # استخدام admin_id بدل id
                nursery = Nursery.objects.get(admin_id__id=nursery_id)  # استخدام admin_id__id
                NurseryParent.objects.update_or_create(
                    nursery=nursery,
                    parent=parent,
                    child=child,
                    defaults={'status': 'pending'}
                )
                return Response({
                    'success': True,
                    'child_id': child.id,
                    'message': f'Request sent to nursery {nursery.name}'
                }, status=status.HTTP_201_CREATED)
            except Nursery.DoesNotExist:
                return Response({
                    'error': 'Nursery not found',
                    'code': 'NOT_FOUND'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'child_id': child.id}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid child data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
        user = parent.admin
        status = request.data.get('status')
        if status not in ['accepted', 'rejected']:  # نزلنا pending
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
        if status not in ['accepted', 'rejected']:  # نزلنا pending
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

class AdminParentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, parent_id=None):
        if parent_id:
            try:
                parent = Parent.objects.get(id=parent_id)  # افتراض إن Parent عنده id كـ Primary Key
                serializer = ParentSerializer(parent)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Parent.DoesNotExist:
                return Response({'error': 'Parent not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        else:
            parents = Parent.objects.filter(status='pending')  # افتراض إن عندك حقل status في Parent
            serializer = ParentSerializer(parents, many=True)
            return Response({
                'pending_parents': serializer.data
            }, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, parent_id):
        try:
            parent = Parent.objects.get(id=parent_id)  # افتراض إن Parent عنده id كـ Primary Key
            requested_status = request.data.get('status')
            if requested_status not in ['accepted', 'rejected']:
                return Response({'error': 'Invalid status', 'code': 'INVALID_STATUS'}, status=status.HTTP_400_BAD_REQUEST)

            parent.status = requested_status  # افتراض إن عندك حقل status في Parent
            parent.save()
            create_notification(
                parent,
                title=f"Parent {requested_status.capitalize()}",
                message=f"Your request as a parent has been {requested_status} by the admin.",
                is_nursery=False
            )
            return Response({'success': True, 'message': f'Parent status updated to {requested_status}'}, status=status.HTTP_200_OK)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent not found', 'code': 'NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

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
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_nursery_requests(request):
    users_with_requests = User.objects.filter(
        nursery_request__isnull=False, nursery_request__ne='', user_type='nursery'
    )
    nurseries = [Nursery.objects.get(admin=user) for user in users_with_requests]
    serializer = NurserySerializer(nurseries, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)


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

# class NurseryInformationView(APIView):
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def post(self, request):
#         user = request.user
#         if user.user_type != 'nursery':
#             return Response({
#                 'error': 'Only nurseries can submit information',
#                 'code': 'UNAUTHORIZED'
#             }, status=403)

#         try:
#             nursery = Nursery.objects.get(admin_id=user)
#         except Nursery.DoesNotExist:
#             return Response({
#                 'error': 'Nursery not found',
#                 'code': 'NOT_FOUND'
#             }, status=404)

#         data = {
#             'name': request.data.get('name', nursery.name),
#             'phone_number': request.data.get('phone', nursery.phone_number),
#             'address': request.data.get('location', nursery.address),
#             'description': request.data.get('description', nursery.description),
#             'longitude': request.data.get('longitude', nursery.longitude),
#             'latitude': request.data.get('latitude', nursery.latitude),
#             'image': request.data.get('photo', nursery.image),
#             'status': 'pending'
#         }
#         serializer = NurserySerializer(nursery, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             admin_users = User.objects.filter(user_type='admin')
#             for admin in admin_users:
#                 create_notification(
#                     admin,
#                     title="New Nursery Information Request",
#                     message=f"Nursery {nursery.name} submitted information for approval.",
#                     is_nursery=False
#                 )
#             return Response({
#                 'success': True,
#                 'message': 'Information submitted for approval',
#                 'nursery_status': 'pending'
#             }, status=200)
#         return Response({
#             'error': 'Invalid data',
#             'details': serializer.errors
#         }, status=400)

#     def get(self, request):
#         user = request.user
#         if user.user_type != 'nursery':
#             return Response({
#                 'error': 'Only nurseries can access this page',
#                 'code': 'UNAUTHORIZED'
#             }, status=403)

#         try:
#             nursery = Nursery.objects.get(admin_id=user)
#             if nursery.status != 'accepted':
#                 return Response({
#                     'error': 'Nursery not approved yet',
#                     'code': 'NOT_APPROVED'
#                 }, status=403)

#             notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
#             menu = [
#                 {'name': 'Home', 'url': '/nursery-information/', 'icon': 'home'},
#                 {'name': 'Edit', 'url': '/nursery-edit/', 'icon': 'edit'},
#                 {'name': 'Dashboard', 'url': f'/nursery-dashboard/{nursery.admin_id.id}/', 'icon': 'dashboard'}
#             ]
#             response_data = {
#                 'success': True,
#                 'nursery_data': {
#                     'name': nursery.name,
#                     'address': nursery.address,
#                     'phone_number': nursery.phone_number,
#                     'status': nursery.status
#                 },
#                 'notifications': NotificationSerializer(notifications, many=True).data,
#                 'menu': menu
#             }
#             return Response(response_data, status=200)
#         except Nursery.DoesNotExist:
#             return Response({
#                 'error': 'Nursery not found',
#                 'code': 'NOT_FOUND'
#             }, status=404)

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

        # Handle image field
        if 'photo' in request.FILES:
            data['image'] = request.FILES['photo']
        elif 'photo' not in request.data:
            data['image'] = nursery.image if nursery.image else None
        else:
            data['image'] = None  # Clear image if explicitly sent as empty

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

        # افترض إن فيه نموذج Notification مرتبط بالـ user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]  # 5 إشعارات أخيرة
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

#//////////////////////////////
class AdminNurseryDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'admin':
            return Response({
                'error': 'Only admins can access this',
                'code': 'UNAUTHORIZED'
            }, status=status.HTTP_403_FORBIDDEN)

        nurseries = Nursery.objects.filter(status='pending')
        serializer = NurserySerializer(nurseries, many=True)
        return Response({
            'success': True,
            'pending_nurseries': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, nursery_id):
        if request.user.user_type != 'admin':
            return Response({
                'error': 'Only admins can access this',
                'code': 'UNAUTHORIZED'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            nursery = Nursery.objects.get(id=nursery_id)
            action = request.data.get('action')

            if action not in ['accept', 'reject']:
                return Response({
                    'error': 'Invalid action',
                    'code': 'INVALID_ACTION'
                }, status=status.HTTP_400_BAD_REQUEST)

            if action == 'accept':
                nursery.status = 'approved'
                message = f"Your nursery information for {nursery.name} has been accepted."
            elif action == 'reject':
                nursery.status = 'rejected'
                message = f"Your nursery information for {nursery.name} has been rejected."

            nursery.save()
            create_notification(
                nursery.admin,
                title=f"Nursery Request {action.capitalize()}",
                message=message,
                is_nursery=True
            )
            return Response({
                'success': True,
                'message': f'Nursery request {action}ed',
                'nursery_status': nursery.status
            }, status=status.HTTP_200_OK)
        except Nursery.DoesNotExist:
            return Response({
                'error': 'Nursery not found',
                'code': 'NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)
        
