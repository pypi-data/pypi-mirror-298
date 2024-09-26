import logging
from functools import wraps
from typing import Type

from flask import jsonify, Request
from pydantic import BaseModel, ValidationError
from requests import HTTPError, RequestException

from easyflowutils.logger_utils import configure_cloud_logger

VALIDATION_ERROR_STATUS_CODE = 422


def validate_request(request_model: Type[BaseModel]):
    VALIDATION_ERROR_STATUS_CODE = 422
    configure_cloud_logger()

    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            try:
                request_json = request.get_json()
                logging.info(f"Received request: {request_json or {} }")
                if not request_json:
                    return jsonify({"error": "Request body is empty"}), VALIDATION_ERROR_STATUS_CODE

                validated_data = request_model(**request_json)

                return func(validated_data, *args, **kwargs)

            except ValidationError as e:
                error_messages = []
                for error in e.errors():
                    error_messages.append(f"{error['loc'][0]}: {error['msg']}")

                error_response = {
                    "error": "Validation failed",
                    "details": error_messages
                }
                logging.warning(f"Validation error: {error_response}")
                return jsonify(error_response), VALIDATION_ERROR_STATUS_CODE

            except HTTPError as e:
                status_code = e.response.status_code if e.response.status_code else 500
                error_message = str(e)
                logging.error(
                    f"HTTP error: {error_message}, status code reutned: {e.response.status_code} ,real one: {status_code}")
                return jsonify({"error": f"An HTTP error occurred: {error_message}"}), status_code

            except RequestException as e:
                logging.error(f"Request error: {str(e)}")
                return jsonify({"error": f"A network error occurred: {str(e)}"}), 503

            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                return jsonify({"error": f"An unexpected error occurred, {str(e)}"}), 500

        return wrapper

    return decorator
