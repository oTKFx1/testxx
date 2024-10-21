from rest_framework import serializers
from .models import ConsultantService, ConsultantDocument, ConsultantChat
from users.models import NormalUserInfo, SpecialistProfile

class ConsultantDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantDocument
        fields = ['id', 'file', 'uploaded_at']


class UserSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class FetchCurrentNormalUserSerializers(serializers.ModelSerializer):
    user = UserSpecialistSerializer(read_only=True)
    class Meta:
        model = NormalUserInfo
        fields = ['user', 'phone_number']

class SpecialistProfileFetchSerializer(serializers.ModelSerializer):
    user = UserSpecialistSerializer(read_only=True)  # Use lowercase and read_only if not writable

    class Meta:
        model = SpecialistProfile
        fields = ['user', 'picture', 'description', 'phone_number', 'experience_years', 'certificate']

class ConsultantChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantChat
        fields = ['id', 'consultant', 'from_user', 'to_user', 'message', 'file', 'read', 'created_at', 'updated_at']

class ConsultantServiceSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(source='user.user.username')
    user = FetchCurrentNormalUserSerializers(read_only=True)
    specialist = SpecialistProfileFetchSerializer(read_only=True) # Assuming NormalUserInfo has a user attribute
    # specialist = serializers.StringRelatedField(source='specialist.specialist_name')  # Adjust according to your field

    documents = ConsultantDocumentSerializer(many=True, read_only=True)  # Nested serializer for documents
    chats = ConsultantChatSerializer(many=True, read_only=True)  # Nested serializer for chats

    class Meta:
        model = ConsultantService
        fields = [
            'id',
            'user',
            'specialist',
            'details',
            'order_status',
            'reference_number',
            'created_at',
            'updated_at',
            'documents',
            'chats',
        ]
