from rest_framework import serializers
from api.models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model - used in profile and nested in messages"""
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password hashing"""
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    username = serializers.CharField(
        min_length=3,
        max_length=150
    )

    class Meta:
        model = Member
        fields = ['username', 'password']

    def create(self, validated_data):
        """Create a new member with hashed password"""
        member = Member(
            username=validated_data['username']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested author information"""
    author = MemberSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new messages"""
    text = serializers.CharField(
        min_length=1,
        max_length=5000
    )
    
    class Meta:
        model = Message
        fields = ['text']