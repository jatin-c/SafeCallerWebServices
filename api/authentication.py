
# authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        User = get_user_model()
        try:
            user_id = validated_token['user_id']
            return User.objects.get(pk=user_id)
        except (User.DoesNotExist, KeyError):
            raise InvalidToken('Token contained invalid user identification.')

    def authenticate(self, request):
        # Perform token-based authentication as usual
        return super().authenticate(request)

