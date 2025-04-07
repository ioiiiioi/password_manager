from rest_framework.exceptions import APIException

class NotFoundExceptions(APIException):
    default_detail = "Data not found."
    default_code = "not_found"
    status_code = 404

class BadRequestExceptions(APIException):
    default_detail = "Request deny, please check the required object."
    default_code = "bad_request"
    status_code = 400

class UnauthorizedExceptions(APIException):
    default_detail = "Unauthorized access."
    default_code = "unauthorized"
    status_code = 401