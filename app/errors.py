"""
Custom Exception Classes and Standardized Error Handlers.
"""
from datetime import datetime, timezone
from flask import jsonify

class APIException(Exception):
    """Base API Exception class with custom HTTP status code and details."""
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or {}

    def to_dict(self):
        payload = {
            "status": "error",
            "code": self.status_code,
            "message": self.message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        if self.errors:
            payload["errors"] = self.errors
        return payload

class ValidationError(APIException):
    """Raised when request payload fails validation rules (400 Bad Request)."""
    def __init__(self, message="Validation Error", errors=None):
        super().__init__(message=message, status_code=400, errors=errors)

class ResourceNotFoundError(APIException):
    """Raised when requested resource does not exist (404 Not Found)."""
    def __init__(self, message="Requested resource was not found"):
        super().__init__(message=message, status_code=404)

class DuplicateResourceError(APIException):
    """Raised when creating/updating resource violates unique constraint (409 Conflict)."""
    def __init__(self, message="Resource with these unique attributes already exists", errors=None):
        super().__init__(message=message, status_code=409, errors=errors)

class MethodNotAllowedError(APIException):
    """Raised when HTTP method is not allowed for the URI (405 Method Not Allowed)."""
    def __init__(self, message="The method is not allowed for the requested URL."):
        super().__init__(message=message, status_code=405)


def register_error_handlers(app):
    """Register custom error handlers with Flask application instance."""

    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        payload = {
            "status": "error",
            "code": 400,
            "message": getattr(error, 'description', 'Bad Request'),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return jsonify(payload), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        payload = {
            "status": "error",
            "code": 404,
            "message": getattr(error, 'description', 'The requested URL was not found on the server.'),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return jsonify(payload), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        payload = {
            "status": "error",
            "code": 405,
            "message": getattr(error, 'description', 'The HTTP method is not allowed for this route.'),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return jsonify(payload), 405

    @app.errorhandler(415)
    def handle_unsupported_media_type(error):
        payload = {
            "status": "error",
            "code": 415,
            "message": "Unsupported Media Type. Request header Content-Type must be application/json",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return jsonify(payload), 415

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        app.logger.error(f"Internal Server Error: {str(error)}")
        payload = {
            "status": "error",
            "code": 500,
            "message": "An unexpected error occurred on the server.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return jsonify(payload), 500
