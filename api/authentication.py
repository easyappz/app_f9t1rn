from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Token, Member


class TokenAuthentication(BaseAuthentication):
    """Custom token authentication for Member model using Token model"""
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

    def authenticate_credentials(self, key):
        """Validate token and return member instance"""
        try:
            token = Token.objects.select_related('member').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token')

        if not token.member:
            raise AuthenticationFailed('User not found')

        return (token.member, token)

    def authenticate_header(self, request):
        """Return authentication header for 401 responses"""
        return self.keyword