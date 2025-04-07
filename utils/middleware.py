import jwt
import json
from typing import Dict
from uuid import uuid4
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.utils.deprecation import MiddlewareMixin
from core.models import User
from utils.exceptions import (
    BadRequestExceptions, 
    UnauthorizedExceptions,
)
from utils.rsa import RSAEnc
from rest_framework.response import Response
from .authentication import UserAuthorization


def _jwt_encoder(payload:Dict):
        JWT_ALGORITHM = settings.SIMPLE_JWT["ALGORITHM"]
        JWT_SECRET = settings.SIMPLE_JWT["SIGNING_KEY"]
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

class UserAuthentication:
    """
    UserAuthentication guide:
        To authenticate user use :
        UserAuthentication(username:str, password:str).authenticate
    """

    def __init__(self, username:str, password:str) -> None:
        self.username = username
        self.password = password

    def check_authentication(self):
        if ("@" in self.username) and ("." in self.username):
            user = self.get_email()
        else:
            user = self.get_username()
        return user

    def get_username(self):
        user = User.objects.filter(username=self.username)
        if not user.exists():
            raise UnauthorizedExceptions(detail="Incorrect username/email or password.", code=401)
        return user.first()

    def get_email(self):
        user = User.objects.filter(email=self.username)
        if not user.exists():
            raise UnauthorizedExceptions(detail="Incorrect username/email or password.", code=401)
        return user.first()

    def create_token(self, user):
        JWT_EXP = timezone.now()+settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        payload = {
			"token_type":"access",
			"jti":uuid4().hex,
			"username":user.username,
			"user_id": user.id.hex,
			"status": user.is_active,
            "is_staff":user.is_staff,
			"exp": JWT_EXP.timestamp()
		}
        token_body = _jwt_encoder(payload=payload)
        token = f"Bearer {token_body}"
        return token


    @property
    def authenticate(self):
        user = self.check_authentication()
        if not user.check_password(self.password):
            raise UnauthorizedExceptions(detail="Incorrect username/email or password.")
        token = self.create_token(user)
        return user, token

class CustomAuthMiddleware(AuthenticationMiddleware):

    def process_request(self, request) -> None:
        # super().process_request(request)
        authorized_class = UserAuthorization()
        user = authorized_class.find_user(request)
        request.user = user
        if request.headers.get("Authorization", False) and ("Token" in request.headers.get("Authorization")):
            if settings.DEBUG:
                request.META["HTTP_IS_ENCRYPTED"] = False
            else:
                request.META["HTTP_IS_ENCRYPTED"] = True
        else:
            request.META["HTTP_IS_ENCRYPTED"] = False


class CustomResponse(MessageMiddleware):
    def process_response(self, request, response):
        code = response.status_code
        response = super().process_response(request, response)
        request_path = request.path.split('/')
        request_path = list(filter(None, request_path))
        if "rest" in request_path and (code not in [400, 401, 403, 404, 500, 501]):
            interceptor = {
                "status":"success",
                "code":response.status_code,
                "detail":None,
                "data":response.data if hasattr(response, 'data') else None,
            }
            setattr(response, "data", interceptor)
            setattr(response, "content", json.dumps(interceptor).encode())

            # TODO : this is for encrypting response data
            # if request.META.get("HTTP_IS_ENCRYPTED", None) and isinstance(response, Response):
            #     response_data = json.dumps(response.data)
            #     if response.status_code not in [400, 401, 404, 500, 501]:
            #         encrypted_response = RSAEnc().arbitrary_encrypt(public_key=request.user.private_metadata["public_key"], data=response_data)
            #         setattr(response, "content", json.dumps(encrypted_response).encode())
            #         setattr(response, "data", encrypted_response)

        return response

