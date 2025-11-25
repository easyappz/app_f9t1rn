import hashlib
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Member


class TokenStorage:
    """Simple in-memory storage for authentication tokens"""
    _tokens = {}

    @classmethod
    def create_token(cls, member):
        """Generate a simple token based on username hash"""
        token = hashlib.sha256(
            f"{member.username}_{member.id}_{member.created_at}".encode()
        ).hexdigest()
        cls._tokens[token] = member.id
        return token

    @classmethod
    def get_member_id(cls, token):
        """Get member ID by token"""
        return cls._tokens.get(token)

    @classmethod
    def delete_token(cls, token):
        """Remove token from storage"""
        if token in cls._tokens:
            del cls._tokens[token]


class TokenAuthentication(BaseAuthentication):
    """Custom token authentication for Member model"""
    keyword = 'Token'

    def authenticate(self, request):
        """Authenticate user by token from Authorization header"""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None

        try:
            # Expected format: "Token <token_value>"
            parts = auth_header.split()
            
            if len(parts) != 2:
                raise AuthenticationFailed('Invalid token header format')
            
            if parts[0] != self.keyword:
                return None
            
            token = parts[1]
            
        except (ValueError, UnicodeDecodeError):
            raise AuthenticationFailed('Invalid token header')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """Validate token and return member instance"""
        member_id = TokenStorage.get_member_id(token)
        
        if not member_id:
            raise AuthenticationFailed('Invalid or expired token')

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (member, token)

    def authenticate_header(self, request):
        """Return authentication header for 401 responses"""
        return self.keyword
