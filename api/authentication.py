from django.db import models
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Member


class MemberToken(models.Model):
    """Token model for Member authentication"""
    key = models.CharField(max_length=40, primary_key=True)
    member = models.OneToOneField(
        Member,
        related_name='auth_token',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'member_tokens'

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        import secrets
        return secrets.token_hex(20)


class MemberTokenAuthentication(BaseTokenAuthentication):
    """Custom token authentication for Member model"""
    model = MemberToken
    keyword = 'Token'

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('member').get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (token.member, token)
