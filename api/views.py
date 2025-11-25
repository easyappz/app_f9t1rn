from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from api.models import Member, Message, Token
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    MemberSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from api.authentication import TokenAuthentication


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
            {'error': 'Username and password are required'},
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
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            member = Member.objects.get(username=username)
            if member.check_password(password):
                token, created = Token.objects.get_or_create(member=member)
                user_data = {
                    'id': member.id,
                    'username': member.username
                }
                return Response(
                    {
                        'token': token.key,
                        'user': user_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Member.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
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


class MessageListView(APIView):
    """
    Get all messages sorted by created_at.
    GET /api/messages/
    Requires authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.select_related('author').all().order_by('created_at')
        
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message.id,
                'text': message.text,
                'author': message.author.username,
                'created_at': message.created_at.isoformat()
            })
        
        return Response(messages_data, status=status.HTTP_200_OK)


class MessageCreateView(APIView):
    """
    Create a new message.
    POST /api/messages/
    Requires authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(author=request.user)
            response_data = {
                'id': message.id,
                'text': message.text,
                'author': message.author.username,
                'created_at': message.created_at.isoformat()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(
            {'error': 'Text field is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
