from rest_framework import serializers
from .models import User, NormalUserInfo, SpecialistProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()  # This will hash the password
        return user

class NormalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUserInfo
        fields = ['user', 'phone_number', 'token']

class SpecialistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistProfile
        fields = ['user', 'picture', 'description', 'phone_number', 'experience_years', 'certificate', 'token']



class UserSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class SpecialistProfileFetchSerializer(serializers.ModelSerializer):
    user = UserSpecialistSerializer(read_only=True)  # Use lowercase and read_only if not writable

    class Meta:
        model = SpecialistProfile
        fields = ['user', 'picture', 'description', 'phone_number', 'experience_years', 'certificate', 'token']
