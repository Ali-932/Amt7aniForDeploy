from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from jose import jwt, JWTError

from config import settings

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_email = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return {'token': 'unauthorized'}

        if user_email:
            return {'email': str(user_email['email'])}


def create_token_for_user(user):
    token = jwt.encode({'email': str(user.email)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token)
    }
