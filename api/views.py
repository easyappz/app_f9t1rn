from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from api.models import Member, Message
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    MemberSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from api.authentication import TokenAuthentication, TokenStorage


class RegisterView(APIView):
    """
    Register a new user and return success message with user data.
    POST /api/register/
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                member = serializer.save()
                user_data = {
                    'id': member.id,
                    'username': member.username
                }
                return Response(
                    {
                        'message': 'User registered successfully',
                        'user': user_data
                    },
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Authenticate user and return token with user data.
    POST /api/login/
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            member = Member.objects.get(username=username)
            if member.check_password(password):
                token = TokenStorage.create_token(member)
                user_data = {
                    'id': member.id,
                    'username': member.username
                }
                return Response(
                    {
                        'token': token,
                        'user': user_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid username or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Member.DoesNotExist:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ProfileView(APIView):
    """
    Get authenticated user profile.
    GET /api/profile/
    Requires authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        member = request.user
        user_data = {
            'id': member.id,
            'username': member.username
        }
        return Response(user_data, status=status.HTTP_200_OK)


class MessageListCreateView(APIView):
    """
    List all messages or create a new message.
    GET /api/messages/ - Get all messages sorted by created_at
    POST /api/messages/ - Create a new message
    Both require authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all messages with user data, sorted by created_at"""
        messages = Message.objects.select_related('member').all().order_by('created_at')
        
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message.id,
                'text': message.text,
                'author': message.member.username,
                'created_at': message.created_at.isoformat()
            })
        
        return Response(messages_data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new message for authenticated user"""
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(member=request.user)
            response_data = {
                'id': message.id,
                'text': message.text,
                'author': message.member.username,
                'created_at': message.created_at.isoformat()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(
            {'error': 'Message text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
