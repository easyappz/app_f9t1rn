from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from api.models import Member, Message
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    MemberSerializer,
    MessageSerializer
)
from api.authentication import MemberToken, MemberTokenAuthentication


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: MessageSerializer}, description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        serializer = MessageSerializer(data)
        return Response(serializer.data)


class RegisterView(APIView):
    """
    Register a new user and return authentication token.
    """

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'}
                        }
                    }
                }
            },
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            token, created = MemberToken.objects.get_or_create(member=member)
            user_data = MemberSerializer(member).data
            return Response(
                {
                    'token': token.key,
                    'user': user_data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Authenticate user and return token.
    """

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'}
                        }
                    }
                }
            },
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
            401: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.validated_data['member']
            token, created = MemberToken.objects.get_or_create(member=member)
            user_data = MemberSerializer(member).data
            return Response(
                {
                    'token': token.key,
                    'user': user_data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileView(APIView):
    """
    Get authenticated user profile.
    """
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: MemberSerializer,
            401: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessagesListView(APIView):
    """
    Get paginated list of chat messages.
    """
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'count': {'type': 'integer'},
                    'next': {'type': 'string', 'nullable': True},
                    'previous': {'type': 'string', 'nullable': True},
                    'results': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'text': {'type': 'string'},
                                'author': {'type': 'string'},
                                'created_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    }
                }
            },
            401: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def get(self, request):
        messages = Message.objects.all().order_by('created_at')
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
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=MessageSerializer,
        responses={
            201: MessageSerializer,
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
            401: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
