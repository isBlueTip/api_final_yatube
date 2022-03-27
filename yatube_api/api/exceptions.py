from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    print('Exception raised: ' + str(response.status_code))

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code != status.HTTP_403_FORBIDDEN:
            response.status_code = status.HTTP_400_BAD_REQUEST

    return response
