import logging

from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Try DRF default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Handle DRF handled exceptions
        if response.data.get("detail"):
            response.data["message"] = response.data["detail"]
            response.data.pop("detail")
        custom_response = {
            "success": False,
            "status_code": response.status_code,
            "code": get_error_code(response.data),
            "error": response.data
            if isinstance(response.data, dict)
            else {"message": response.data},
        }
        response.data = custom_response
    else:
        # Catch unhandled server exceptions (500)
        view = context.get("view")
        request = context.get("request")

        # Log traceback
        logger.error(
            f"Unhandled Exception in {view.__class__.__name__ if view else 'UnknownView'} "  # noqa: G004
            f"at path {request.path if request else 'unknown'}: {exc}",
            exc_info=True,  # noqa: LOG014
        )

        response = Response(
            {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "code": "server_error",
                "error": {"message": "Internal Server Error."},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


def get_error_code(response_data):
    if isinstance(response_data, str):
        return "error"
    for error in response_data.values():
        if isinstance(error, list) and error and isinstance(error[0], ErrorDetail):
            return error[0].code
        if isinstance(error, ErrorDetail):
            return error.code
    return ""


class PaymentRequiredError(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = "Purchase a request or request pack to send or receive request."
    default_code = "payment_required"

    def __init__(self, detail=default_detail, code=default_code):
        if isinstance(detail, dict):
            for key in detail:
                detail[key] = [ErrorDetail(detail[key], code)]
        self.detail = detail
        self.code = code
        super().__init__(detail=detail, code=code)


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "The request already processed."
    default_code = "conflict"

    def __init__(self, detail=default_detail, code=default_code):
        if isinstance(detail, dict):
            for key in detail:
                detail[key] = [ErrorDetail(detail[key], code)]
        self.detail = detail
        self.code = code
        super().__init__(detail=detail, code=code)
