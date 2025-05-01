from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from .models import Parent, Nursery
# from .serializer import ParentSerializer, NurserySerializer
# from rest_framework.permissions import AllowAny
# import uuid
# from django.core.mail import send_mail
# from accounts.models import User

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Parent.objects.filter(user=self.request.user)

# class NurseryViewSet(viewsets.ModelViewSet):
#     queryset = Nursery.objects.all()
#     serializer_class = NurserySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Nursery.objects.filter(user=self.request.user)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('username')  
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#         except User.DoesNotExist:
#             user = None
#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class SignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("Received data:", request.data)
#         serializer = ParentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 parent = serializer.save()
#                 token, created = Token.objects.get_or_create(user=parent.user)
#                 return Response({
#                     'token': token.key,
#                     'user_id': parent.user.id,
#                     'parent_id': parent.id,
#                     'full_name': parent.full_name,
#                     'email': parent.email,
#                     'phone_number': parent.phone_number
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         print("Serializer errors:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NurserySignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("Received data:", request.data)
        
#         user_data = {
#             'username': request.data.get('email'),
#             'email': request.data.get('email'),
#             'password': request.data.get('password'),
#             'user_type': 'nursery'
#         }
#         try:
#             user = User.objects.create_user(**user_data)
#         except Exception as e:
#             return Response({'error': f'Failed to create user: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         parent_data = {
#             'user': user,
#             'full_name': request.data.get('full_name', 'Nursery Owner'),
#             'email': request.data.get('email'),
#             'phone_number': request.data.get('phone_number'),
#             'children_count': 0
#         }
#         try:
#             parent = Parent.objects.create(**parent_data)
#         except Exception as e:
#             user.delete()
#             return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        
#         nursery_data = {
#             'user': user,
#             'name': request.data.get('full_name'),
#             'location': request.data.get('location', 'Unknown'),
#             'phone': request.data.get('phone_number'),
#             'capacity': request.data.get('capacity', 20)
#         }
#         try:
#             nursery = Nursery.objects.create(**nursery_data)
#         except Exception as e:
#             parent.delete()
#             user.delete()
#             return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'message': 'Nursery registered successfully'
#         }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def password_reset_request(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             user.reset_token = token
#             user.save()
#             send_mail(
#                 'Password Reset Request',
#                 f'Use this token to reset your password: {token}',
#                 'from@example.com',
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import AllowAny
# import uuid
# from django.core.mail import send_mail
# from .models import Parent, Nursery, User
# from .serializers import ParentSerializer, NurserySerializer

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Parent.objects.filter(user=self.request.user)

# class NurseryViewSet(viewsets.ModelViewSet):
#     queryset = Nursery.objects.all()
#     serializer_class = NurserySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Nursery.objects.filter(user=self.request.user)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'message': 'Login successful'
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class SignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("Received data:", request.data)
#         serializer = ParentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 parent = serializer.save()
#                 refresh = RefreshToken.for_user(parent.user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                     'user_id': parent.user.id,
#                     'parent_id': parent.id,
#                     'full_name': parent.full_name,
#                     'email': parent.user.email,
#                     'phone_number': parent.phone_number
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         print("Serializer errors:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NurserySignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("Received data:", request.data)

#         # إنشاء Parent باستخدام ParentSerializer
#         parent_data = {
#             'full_name': request.data.get('full_name', 'Nursery Owner'),
#             'email': request.data.get('email'),
#             'phone_number': request.data.get('phone_number'),
#             'password': request.data.get('password'),
#             'children_count': 0
#         }
#         parent_serializer = ParentSerializer(data=parent_data)
#         if not parent_serializer.is_valid():
#             print("Parent serializer errors:", parent_serializer.errors)
#             return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             parent = parent_serializer.save()
#             user = parent.user
#         except Exception as e:
#             return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         # إنشاء Nursery باستخدام NurserySerializer
#         nursery_data = {
#             'user': user.id,
#             'name': request.data.get('full_name'),
#             'location': request.data.get('location', 'Unknown'),
#             'phone': request.data.get('phone_number'),
#             'capacity': request.data.get('capacity', 20)
#         }
#         nursery_serializer = NurserySerializer(data=nursery_data)
#         if not nursery_serializer.is_valid():
#             print("Nursery serializer errors:", nursery_serializer.errors)
#             parent.user.delete()
#             return Response(nursery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             nursery_serializer.save()
#         except Exception as e:
#             parent.user.delete()
#             return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'message': 'Nursery registered successfully'
#         }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def password_reset_request(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             user.reset_token = token
#             user.save()
#             # send_mail(
#             #     'Password Reset Request',
#             #     f'Use this token to reset your password: {token}',
#             #     'from@example.com',
#             #     [email],
#             #     fail_silently=False,
#             # )
#             return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# تعديلللللللللللللللللل

# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# import uuid
# from django.core.mail import send_mail
# from .models import Parent, Nursery, User
# from .serializers import ParentSerializer, NurserySerializer, UserSerializer

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Parent.objects.filter(user=self.request.user)

# class NurseryViewSet(viewsets.ModelViewSet):
#     queryset = Nursery.objects.all()
#     serializer_class = NurserySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Nursery.objects.filter(user=self.request.user)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if not email or not password:
#             return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

#         user = authenticate(request, username=user.username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user_id': user.id,
#                 'user_type': user.user_type,
#                 'message': 'Login successful'
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class SignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         required_fields = ['email', 'password', 'full_name', 'phone_number']
#         for field in required_fields:
#             if field not in request.data:
#                 return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = ParentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 parent = serializer.save()
#                 refresh = RefreshToken.for_user(parent.user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                     'user_id': parent.user.id,
#                     'parent_id': parent.id,
#                     'full_name': parent.full_name,
#                     'email': parent.user.email,
#                     'phone_number': parent.phone_number,
#                     'message': 'Parent registered successfully'
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NurserySignUpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         required_fields = ['email', 'password', 'full_name', 'phone_number']
#         for field in required_fields:
#             if field not in request.data:
#                 return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

#         # إنشاء User مباشرة
#         user_data = {
#             'email': request.data.get('email'),
#             'password': request.data.get('password'),
#             'username': request.data.get('email'),
#             'user_type': 'nursery'
#         }
#         user_serializer = UserSerializer(data=user_data)
#         if not user_serializer.is_valid():
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = user_serializer.save()
#         except Exception as e:
#             return Response({'error': f'Failed to create user: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         # إنشاء Nursery
#         nursery_data = {
#             'user': user.id,
#             'name': request.data.get('full_name'),
#             'location': request.data.get('location', 'Unknown'),
#             'phone': request.data.get('phone_number'),
#             'capacity': request.data.get('capacity', 20)
#         }
#         nursery_serializer = NurserySerializer(data=nursery_data)
#         if not nursery_serializer.is_valid():
#             user.delete()
#             return Response(nursery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             nursery_serializer.save()
#         except Exception as e:
#             user.delete()
#             return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user_id': user.id,
#             'nursery_name': nursery_data['name'],
#             'email': user.email,
#             'message': 'Nursery registered successfully'
#         }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def password_reset_request(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         if not email:
#             return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             user.reset_token = token
#             user.save()
#             send_mail(
#                 'Password Reset Request',
#                 f'Use this token to reset your password: {token}',
#                 'from@example.com',
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def password_reset_confirm(request):
#     if request.method == 'POST':
#         token = request.data.get('token')
#         new_password = request.data.get('new_password')
#         if not token or not new_password:
#             return Response({'error': 'Token and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(reset_token=token)
#             user.set_password(new_password)
#             user.reset_token = None
#             user.save()
#             return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import AllowAny
# import uuid
# from django.core.mail import send_mail
# from .models import Parent, Nursery, User
# from .serializers import ParentSerializer, NurserySerializer
# from django.views.decorators.csrf import csrf_exempt

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Parent.objects.filter(user=self.request.user)

# class NurseryViewSet(viewsets.ModelViewSet):
#     queryset = Nursery.objects.all()
#     serializer_class = NurserySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Nursery.objects.filter(user=self.request.user)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'message': 'Login successful'
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class SignUpView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         print("Received data:", request.data)
#         serializer = ParentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 parent = serializer.save()
#                 refresh = RefreshToken.for_user(parent.user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                     'user_id': parent.user.id,
#                     'parent_id': parent.id,
#                     'full_name': parent.full_name,
#                     'email': parent.user.email,
#                     'phone_number': parent.phone_number
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         print("Serializer errors:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NurserySignUpView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         print("Received data:", request.data)

#         # إنشاء Parent باستخدام ParentSerializer
#         parent_data = {
#             'full_name': request.data.get('full_name', 'Nursery Owner'),
#             'email': request.data.get('email'),
#             'phone_number': request.data.get('phone_number'),
#             'password': request.data.get('password'),
#             'children_count': 0
#         }
#         parent_serializer = ParentSerializer(data=parent_data)
#         if not parent_serializer.is_valid():
#             print("Parent serializer errors:", parent_serializer.errors)
#             return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             parent = parent_serializer.save()
#             user = parent.user
#         except Exception as e:
#             return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         # إنشاء Nursery باستخدام NurserySerializer
#         nursery_data = {
#             'user': user.id,
#             'name': request.data.get('full_name'),
#             'location': request.data.get('location', 'Unknown'),
#             'phone': request.data.get('phone_number'),
#             'capacity': request.data.get('capacity', 20)
#         }
#         nursery_serializer = NurserySerializer(data=nursery_data)
#         if not nursery_serializer.is_valid():
#             print("Nursery serializer errors:", nursery_serializer.errors)
#             parent.user.delete()
#             return Response(nursery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             nursery_serializer.save()
#         except Exception as e:
#             parent.user.delete()
#             return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'message': 'Nursery registered successfully'
#         }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def password_reset_request(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             user.reset_token = token
#             user.save()
#             # send_mail(
#             #     'Password Reset Request',
#             #     f'Use this token to reset your password: {token}',
#             #     'from@example.com',
#             #     [email],
#             #     fail_silently=False,
#             # )
#             return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import AllowAny
# import uuid
# from django.core.mail import send_mail
# from .models import Parent, Nursery, User
# from .serializers import ParentSerializer, NurserySerializer
# from django.views.decorators.csrf import csrf_exempt

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Parent.objects.filter(user=self.request.user)

# class NurseryViewSet(viewsets.ModelViewSet):
#     queryset = Nursery.objects.all()
#     serializer_class = NurserySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Nursery.objects.filter(user=self.request.user)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('email')  # تعديل من username لـ email
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'token': str(refresh.access_token),  # تعديل ليترجع token
#                 'user_id': user.id,  # إضافة user_id
#                 'message': 'Login successful'
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class SignUpView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         print("Received data:", request.data)
#         serializer = ParentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 parent = serializer.save()
#                 refresh = RefreshToken.for_user(parent.user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                     'user_id': parent.user.id,
#                     'parent_id': parent.id,
#                     'full_name': parent.full_name,
#                     'email': parent.user.email,
#                     'phone_number': parent.phone_number
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         print("Serializer errors:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NurserySignUpView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         print("Received data:", request.data)

#         # إنشاء Parent باستخدام ParentSerializer
#         parent_data = {
#             'full_name': request.data.get('full_name', 'Nursery Owner'),
#             'email': request.data.get('email'),
#             'phone_number': request.data.get('phone_number'),
#             'password': request.data.get('password'),
#             'children_count': 0
#         }
#         parent_serializer = ParentSerializer(data=parent_data)
#         if not parent_serializer.is_valid():
#             print("Parent serializer errors:", parent_serializer.errors)
#             return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             parent = parent_serializer.save()
#             user = parent.user
#         except Exception as e:
#             return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         # إنشاء Nursery باستخدام NurserySerializer
#         nursery_data = {
#             'user': user.id,
#             'name': request.data.get('full_name'),
#             'location': request.data.get('location', 'Unknown'),
#             'phone': request.data.get('phone_number'),
#             'capacity': request.data.get('capacity', 20)
#         }
#         nursery_serializer = NurserySerializer(data=nursery_data)
#         if not nursery_serializer.is_valid():
#             print("Nursery serializer errors:", nursery_serializer.errors)
#             parent.user.delete()
#             return Response(nursery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             nursery_serializer.save()
#         except Exception as e:
#             parent.user.delete()
#             return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'message': 'Nursery registered successfully'
#         }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def password_reset_request(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             user.reset_token = token
#             user.save()
#             # send_mail(
#             #     'Password Reset Request',
#             #     f'Use this token to reset your password: {token}',
#             #     'from@example.com',
#             #     [email],
#             #     fail_silently=False,
#             # )
#             return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         email = request.data.get('email')
#         new_password = request.data.get('new_password')
#         try:
#             user = User.objects.get(email=email)
#             user.set_password(new_password)
#             user.save()
#             return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class ParentResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         email = request.data.get('email')
#         new_password = request.data.get('new_password')
#         try:
#             user = User.objects.get(email=email)
#             parent = Parent.objects.filter(user=user).first()
#             if not parent:
#                 return Response({'error': 'Parent not found'}, status=status.HTTP_404_NOT_FOUND)
#             user.set_password(new_password)
#             user.save()
#             return Response({'message': 'Parent password reset successful'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

        # إنشاء Parent باستخدام ParentSerializer
        parent_data = {
            'full_name': request.data.get('nursery_name', 'Nursery Owner'),
            'email': request.data.get('email'),
            'phone_number': request.data.get('phone_number'),
            'password': request.data.get('password'),
            'children_count': 0
        }
        parent_serializer = ParentSerializer(data=parent_data)
        if not parent_serializer.is_valid():
            print("Parent serializer errors:", parent_serializer.errors)
            return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            parent = parent_serializer.save()
            user = parent.user
        except Exception as e:
            return Response({'error': f'Failed to create parent: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء Nursery باستخدام NurserySerializer
        nursery_data = {
            'user': user.id,
            'name': request.data.get('nursery_name'),
            'location': request.data.get('location', 'Unknown'),
            'phone': request.data.get('phone_number'),
            'capacity': request.data.get('capacity', 20)
        }
        nursery_serializer = NurserySerializer(data=nursery_data)
        if not nursery_serializer.is_valid():
            print("Nursery serializer errors:", nursery_serializer.errors)
            parent.user.delete()
            return Response(nursery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            nursery = nursery_serializer.save()
        except Exception as e:
            parent.user.delete()
            return Response({'error': f'Failed to create nursery: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user_id': user.id,
            'nursery_id': nursery.id,
        }, status=status.HTTP_201_CREATED)

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
            # send_mail(
            #     'Password Reset Request',
            #     f'Use this token to reset your password: {token}',
            #     'from@example.com',
            #     [email],
            #     fail_silently=False,
            # )
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