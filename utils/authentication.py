import time
import os
import jwt
from django.contrib.auth.models import AnonymousUser
from core.models import User
from utils.exceptions import (
    BadRequestExceptions, 
    UnauthorizedExceptions,
)
from rest_framework.authentication import TokenAuthentication
from dotenv import load_dotenv

load_dotenv()

class UserAuthorization(TokenAuthentication):
    keyword = "Token"

    def _decode_jwt(self, token):
        JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
        JWT_SECRET = os.getenv('SECRET_KEY')
        try:
            decoded_msg = jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])
        except Exception as e:
            raise UnauthorizedExceptions(detail="Bad jwt token.")
        
        return decoded_msg

    def find_user(self, request):
        headers = request.headers
        authorization = headers.get("Authorization", None)

        if authorization: 
            types, token = authorization.split()
            if types not in ("Token","Bearer",):
                raise BadRequestExceptions(detail="Wrong token scheme.")
            
            decoded_msg = self._decode_jwt(token)
            if decoded_msg["exp"] < time.time():
                raise UnauthorizedExceptions(detail="Token was expired.")

            user = User.objects.filter(id=decoded_msg["user_id"], is_active=True)
            if not user.exists():
                raise UnauthorizedExceptions(detail="User is registered or is not active yet.")
            return user.first()
        else:
            return AnonymousUser()

    def authenticate(self, request):
        host = request.get_full_path().split('/')
        host.remove("")
        user = self.find_user(request)
        if host[0] == 'schema':
            return
        if isinstance(user, User):
            return (user, None)
        else:
            raise UnauthorizedExceptions(detail="Need access token.")
