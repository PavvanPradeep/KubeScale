from jwt.exceptions import InvalidTokenError
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .validation import custom_validation, validate_email, validate_password
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
import jwt
from django.conf import settings

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	@csrf_exempt
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    @csrf_exempt
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            
            # Check if the user is authenticated (i.e., exists)
            if user is not None:
                login(request, user)
                
                # Generate JWT token
                token = self.generate_jwt_token(user.email)
                
                response = Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
                
                # Set JWT token as a cookie
                response.set_cookie(key='jwt', value=token.decode('utf-8'), httponly=True, expires=datetime.now() + timedelta(days=7))
                
                return response
            else:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    def generate_jwt_token(self, email):
        token = jwt.encode({'email': email}, settings.SECRET_KEY, algorithm='HS256')
        return token



class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	@csrf_exempt
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)



class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        # Get the JWT token from the request cookies
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token is expired.')
        except InvalidTokenError as e:
            raise AuthenticationFailed(f'Token is invalid: {e}')

        # Fetch the user based on the user_id from the token
        user = User.objects.filter(email=payload['email']).first()
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
    
from django.http import JsonResponse
from datetime import datetime, timedelta

def delete_cookie(request):
    response = JsonResponse({'message': 'Cookie deleted'})
    response.delete_cookie('jwt')
    return response


