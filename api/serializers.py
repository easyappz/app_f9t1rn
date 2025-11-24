from rest_framework import serializers
from api.models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username']
        read_only_fields = ['id']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=150,
        required=True
    )
    password = serializers.CharField(
        min_length=6,
        required=True,
        write_only=True
    )

    def validate_username(self, value):
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        member = Member(
            username=validated_data['username']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")

        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not member.check_password(password):
            raise serializers.ValidationError("Invalid username or password")

        data['member'] = member
        return data


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def get_author(self, obj):
        return obj.author.username

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
