from rest_framework import serializers
from .models import ConsultantService, ConsultantDocument, ConsultantChat
from users.models import NormalUserInfo, SpecialistProfile

class ConsultantDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantDocument
        fields = ['id', 'file', 'uploaded_at']


class ConsultantChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantChat
        fields = ['id', 'consultant', 'from_user', 'to_user', 'message', 'file', 'read', 'created_at', 'updated_at']

class ConsultantServiceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.user.username')  # Assuming NormalUserInfo has a user attribute
    specialist = serializers.StringRelatedField(source='specialist.specialist_name')  # Adjust according to your field

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
