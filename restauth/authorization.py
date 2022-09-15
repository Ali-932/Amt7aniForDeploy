from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from jose import jwt, JWTError

from config import settings

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return None

        if user:
            return {'user_id': str(user['user_id']),'user_email': str(user['user_email'])}


def create_token_for_user(user):
    token = jwt.encode({'user_id': str(user.id),'user_email':str(user.email)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token)
    }

