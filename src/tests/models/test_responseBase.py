from schemas.responseBase import BaseResponse
import pytest
from datetime import datetime, timezone


def test_default_values():
    """ Test the default values of fields """
    response = BaseResponse()
    assert response.statusCode == 200
    assert response.responseType == "success"
    assert not response.isError
    assert isinstance(response.traceId, str) and len(response.traceId) > 0
    # Check if the timestamp is a recent timestamp (assuming the test runs soon after creation)
    assert datetime.fromisoformat(response.timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)


def test_get_status_code_default():
    """ Test the class method getStatusCodeDefault """
    assert BaseResponse.getStatusCodeDefault() == 200


def test_get_response_type_exception_default():
    """ Test the class method getResponseTypeExceptionDefault """
    assert BaseResponse.getResponseTypeExceptionDefault() == "success"


def test_trace_id_unique():
    """ Test that each traceId is unique """
    response1 = BaseResponse()
    response2 = BaseResponse()
    assert response1.traceId != response2.traceId


@pytest.mark.parametrize("code, response_type, is_error", [
    (500, "error", True),
    (404, "not found", False),
    (403, "forbidden", True),
])
def test_custom_values(code, response_type, is_error):
    """ Test the initialization with custom values """
    response = BaseResponse(statusCode=code, responseType=response_type, isError=is_error)
    assert response.statusCode == code
    assert response.responseType == response_type
    assert response.isError == is_error
