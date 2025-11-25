from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
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
                    {'error': 'User with this username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Handle validation errors
        errors = serializer.errors
        if 'username' in errors or 'password' in errors:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Authenticate user and return token with user data.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
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
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Member.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    """
    Get authenticated user profile.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        member = request.user
        return Response(
            {
                'id': member.id,
                'username': member.username,
                'created_at': member.created_at.isoformat()
            },
            status=status.HTTP_200_OK
        )


class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageListView(APIView):
    """
    Get paginated list of chat messages.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get(self, request):
        messages = Message.objects.select_related('member').all().order_by('timestamp')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(messages, request)
        
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageCreateView(APIView):
    """
    Create a new chat message.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(member=request.user)
            response_data = {
                'id': message.id,
                'username': message.member.username,
                'text': message.text,
                'timestamp': message.timestamp.isoformat()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        if 'text' in serializer.errors:
            return Response(
                {'error': 'Text field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
