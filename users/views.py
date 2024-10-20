from django.shortcuts import render
from django.http import HttpResponse
from . import serializers
from django.contrib.auth.hashers import check_password

# Rest frameworks Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Extra Imports
from .models import User, NormalUserInfo, SpecialistProfile
from django.db.models import Q  # Import Q for complex queries
import secrets
# Create your views here.
def welcome(request):

    return HttpResponse('Welcome! Users')


@api_view(['POST'])
def signup(request):
    # Get role from the request
    role = request.data.get('role')
    
    # Serialize the user data
    user_serializer = serializers.UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        
        # Token to be used in the profile
        token = secrets.token_hex(16)  # Generate a token here

        # Handle additional info based on the role
        if role == 'User':
            normal_user_info_serializer = serializers.NormalUserInfoSerializer(data={
                'user': user.id,
                'phone_number': request.data.get('phone_number'),
                'token': token
            })
            if normal_user_info_serializer.is_valid():
                normal_user_info_serializer.save()
                return Response({'message': 'User created successfully!', 'token': token}, status=status.HTTP_201_CREATED)
            else:
                # Delete the user if the profile creation fails
                user.delete()
                return Response(normal_user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif role == 'Specialist':
            specialist_profile_serializer = serializers.SpecialistProfileSerializer(data={
                'user': user.id,
                'picture': request.data.get('picture'),
                'description': request.data.get('description'),
                'phone_number': request.data.get('phone_number'),
                'experience_years': request.data.get('experience_years'),
                'certificate': request.data.get('certificate'),
                'token': token
            })
            if specialist_profile_serializer.is_valid():
                specialist_profile_serializer.save()
                return Response({'message': 'Specialist created successfully!', 'token': token}, status=status.HTTP_201_CREATED)
            else:
                # Delete the user if the profile creation fails
                user.delete()
                return Response(specialist_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif role == 'Company':
            return Response({'message': 'Company signup is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    # Get identifier and password from the request
    identifier = request.data.get('identifier')  # This can be username, email, or phone number
    password = request.data.get('password')

    # Try to find the user by username, email, or phone number
    try:
        user = User.objects.get(
            Q(username=identifier) | 
            Q(email=identifier) |
            Q(additional_info__phone_number=identifier)  # Assuming related name for phone number
        )
    except User.DoesNotExist:
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the password matches
    if check_password(password, user.password):  # Assuming you have a check_password method
        # Generate a new token for the user
        token = secrets.token_hex(16)

        # Update the token in the respective profile based on user role
        if user.role == 'User':
            normal_user_info = user.additional_info
            normal_user_info.token = token
            normal_user_info.save()
        elif user.role == 'Specialist':
            specialist_profile = user.specialist_profile
            specialist_profile.token = token
            specialist_profile.save()

        return Response({'message': 'Login successful!', 'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    # Get the token from the request
    token = request.data.get('token')

    if not token:
        return Response({'message': 'Token is required for logout!'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find the user associated with the token
    try:
        # Check if it's a normal user
        normal_user_info = NormalUserInfo.objects.get(token=token)
        normal_user_info.token = ''  # Clear the token
        normal_user_info.save()
    except NormalUserInfo.DoesNotExist:
        try:
            # Check if it's a specialist
            specialist_profile = SpecialistProfile.objects.get(token=token)
            specialist_profile.token = ''  # Clear the token
            specialist_profile.save()
        except SpecialistProfile.DoesNotExist:
            return Response({'message': 'Invalid token!'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)
