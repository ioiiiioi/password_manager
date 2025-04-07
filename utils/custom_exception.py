from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data.get("detail", None)
        code = response.status_code
        response = {
            "status":"error",
            "code":response.status_code,
            "detail":detail,
            "data":{},
        }
        return Response(response, status=code)
    return response