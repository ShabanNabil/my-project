# # تعديل يوم الاربعععععععععععع
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User, Nursery, Parent, Child, Visit, Notification
from .serializers import UserSerializer, NurserySerializer, ParentSerializer, ChildSerializer, VisitSerializer, NotificationSerializer
import uuid
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

class SignUpView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        print("Received data:", request.data)
        user_data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
                parent_data = {
                    'admin_id': user.id,
                    'name': request.data.get('name'),
                    'address': request.data.get('address', 'Unknown'),
                    'phone': request.data.get('phone'),
                    'job': request.data.get('job', '')
                }
                parent_serializer = ParentSerializer(data=parent_data)
                if parent_serializer.is_valid():
                    parent = parent_serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'success': True,
                        'token': str(refresh.access_token),
                        'user_id': user.id,
                        'parent_id': parent.id,
                    }, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        print("User serializer errors:", user_serializer.errors)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NurserySignUpView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        print("Received data:", request.data)
        user_data = {
            'name': request.data.get('full_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
                nursery_data = {
                    'admin_id': user.id,
                    'name': request.data.get('full_name'),
                    'email': request.data.get('email'),
                    'phone': request.data.get('phone_number'),
                    'address': request.data.get('location', 'Unknown'),
                    'description': request.data.get('description', ''),
                    'longitude': request.data.get('longitude'),
                    'latitude': request.data.get('latitude')
                }
                serializer = NurserySerializer(data=nursery_data)
                if serializer.is_valid():
                    nursery = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'success': True,
                        'token': str(refresh.access_token),
                        'user_id': user.id,
                        'nursery_id': nursery.id,
                    }, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        print("User serializer errors:", user_serializer.errors)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_parent_view(request):
    if request.method == 'POST':
        print("Received login data for parent:", request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            print("Missing email or password:", {'email': email, 'password': password})
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            parent = Parent.objects.filter(admin=user).first()
            if not parent:
                return Response({'error': 'User is not a parent'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=user.email, password=password)
        except User.DoesNotExist:
            print("User does not exist for email:", email)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Login successful for parent'
            }, status=status.HTTP_200_OK)
        print("Authentication failed for email:", email)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_nursery_view(request):
    if request.method == 'POST':
        print("Received login data for nursery:", request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            print("Missing email or password:", {'email': email, 'password': password})
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            nursery = Nursery.objects.filter(admin=user).first()
            if not nursery:
                return Response({'error': 'User is not a nursery'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=user.email, password=password)
        except User.DoesNotExist:
            print("User does not exist for email:", email)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Login successful for nursery'
            }, status=status.HTTP_200_OK)
        print("Authentication failed for email:", email)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_admin_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if not user.is_staff or not user.is_superuser:
                return Response({'error': 'User is not an admin'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=user.email, password=password)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Login successful for admin'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def password_reset_request(request):
    if request.method == 'POST':
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
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        reset_token = request.data.get('reset_token')
        try:
            user = User.objects.get(email=email, reset_token=reset_token)
            user.set_password(new_password)
            user.reset_token = None
            user.save()
            return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or token'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ParentResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        reset_token = request.data.get('reset_token')
        try:
            user = User.objects.get(email=email, reset_token=reset_token)
            parent = Parent.objects.filter(admin=user).first()
            if not parent:
                return Response({'error': 'Parent not found'}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            user.reset_token = None
            user.save()
            return Response({'success': True, 'message': 'Parent password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or token'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ParentViewSet(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return Parent.objects.all()
        return Parent.objects.filter(admin=user)


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
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        nursery.status = status
        nursery.save()

        Notification.objects.create(
            nursery=nursery,
            title=f"Nursery {status.capitalize()}",
            message=f"Your nursery {nursery.name} has been {status} by the admin.",
            is_read=False
        )

        return Response({'success': True, 'message': f'Nursery status updated to {status}'}, status=status.HTTP_200_OK)

# إدارة الأطفال
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
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        child.status = status
        child.save()

        Notification.objects.create(
            parent=child.parent,
            title=f"Child {status.capitalize()}",
            message=f"Your child {child.first_name} {child.family_name} has been {status} by the nursery.",
            is_read=False
        )

        return Response({'success': True, 'message': f'Child status updated to {status}'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(parent=Parent.objects.get(admin=self.request.user))


class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return Visit.objects.all()
        return Visit.objects.filter(nursery__admin=user) | Visit.objects.filter(parent__admin=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        visit = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        visit.status = status
        visit.save()

        Notification.objects.create(
            parent=visit.parent,
            title=f"Visit {status.capitalize()}",
            message=f"Your visit request on {visit.visit_date} has been {status} by the nursery.",
            is_read=False
        )

        return Response({'success': True, 'message': f'Visit status updated to {status}'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(parent=Parent.objects.get(admin=self.request.user))


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(parent__admin=user) | Notification.objects.filter(nursery__admin=user)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'success': True, 'message': 'Notification marked as read'}, status=status.HTTP_200_OK)