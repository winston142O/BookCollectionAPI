import traceback
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from .serializers import userSerializer
from rest_framework.exceptions import AuthenticationFailed

# View type.
@api_view(['POST'])
# Use of decorator to establish public access to registration.
@permission_classes([AllowAny])
def signup(request):
    try:
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.has_usable_password():
                login(request, user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data provided.', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        return Response({'error': 'User with this username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An unexpected error occurred during user registration.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View type.
@api_view(['POST'])
# Use of decorator to establish public access to registration.
@permission_classes([AllowAny])
def login_view(request):
    try:
        # Retrive the given user and password.
        username = request.data.get('username')
        password = request.data.get('password')
        # Validate
        user = authenticate(request, username=username, password=password)
        if user:
            # If the credentials are correct, user is returned and logged-in.
            login(request, user)
            # Retrieve Token/Create if inexistent.
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    except AuthenticationFailed:
        return Response({'error': 'Authentication failed. Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An internal server error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View type.
@api_view(['GET'])
# Use of decorator to establish that only authenticated users can access.
@permission_classes([IsAuthenticated])
def get_user_details(request):
    try:
        # Serialize and retrieve current user's details.
        user_serializer = userSerializer(request.user)
        return Response({'user': user_serializer.data})
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An unexpected error occurred while fetching user details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
