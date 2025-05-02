from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import uuid
from django.core.mail import send_mail
from .models import Parent, Nursery, User
from .serializers import ParentSerializer, NurserySerializer
from django.views.decorators.csrf import csrf_exempt

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Parent.objects.filter(user=self.request.user)

class NurseryViewSet(viewsets.ModelViewSet):
    queryset = Nursery.objects.all()
    serializer_class = NurserySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Nursery.objects.filter(user=self.request.user)

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
            parent = Parent.objects.filter(user=user).first()
            if not parent:
                return Response({'error': 'User is not a parent'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=user.username, password=password)
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
            nursery = Nursery.objects.filter(user=user).first()
            if not nursery:
                return Response({'error': 'User is not a nursery'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=user.username, password=password)
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

class SignUpView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        print("Received data:", request.data)
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                parent = serializer.save()
                refresh = RefreshToken.for_user(parent.user)
                return Response({
                    'success': True,
                    'token': str(refresh.access_token),
                    'user_id': parent.user.id,
                    'parent_id': parent.id,
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NurserySignUpView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        print("Received data:", request.data)
        nursery_data = {
            'name': request.data.get('full_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone_number'),
            'password': request.data.get('password'),
            'location': request.data.get('location', 'Unknown'),
            'capacity': request.data.get('capacity', 20)
        }
        serializer = NurserySerializer(data=nursery_data)
        if serializer.is_valid():
            try:
                nursery = serializer.save()
                refresh = RefreshToken.for_user(nursery.user)
                return Response({
                    'success': True,
                    'token': str(refresh.access_token),
                    'user_id': nursery.user.id,
                    'parent_id': nursery.id,
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
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
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ParentResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            parent = Parent.objects.filter(user=user).first()
            if not parent:
                return Response({'error': 'Parent not found'}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            user.save()
            return Response({'success': True, 'message': 'Parent password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)