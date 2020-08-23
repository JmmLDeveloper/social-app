from rest_framework import authentication
from rest_framework import exceptions
from .models import User
from django.conf import settings
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = None
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        except Exception:
            return (None, None)

        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=data.get('sub'))
            return (user, token)
        except Exception:
            raise exceptions.AuthenticationFailed("Couldn't Authenticate")
