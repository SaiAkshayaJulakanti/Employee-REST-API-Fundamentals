"""
Flask Application Factory Package Initializer.
"""
import time
from flask import Flask, jsonify, request
from app.config import config_by_name
from app.database import db
from app.utils.logger import setup_logger
from app.errors import register_error_handlers
from app.routes.employee_routes import employee_bp

def create_app(config_name='dev'):
    """
    Application Factory function for Flask.
    """
    app = Flask(__name__)
    
    # Load configuration
    config_cls = config_by_name.get(config_name, config_by_name['dev'])
    app.config.from_object(config_cls)

    # Initialize extensions
    db.init_app(app)

    # Setup Logging
    setup_logger(app)

    # Register Error Handlers
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(employee_bp)

    # Global Before Request Hook (Logging & Timing)
    @app.before_request
    def before_request_hook():
        request.start_time = time.time()
        app.logger.debug(f"Incoming HTTP Request: {request.method} {request.path} from IP={request.remote_addr}")

    # Global After Request Hook (Logging Execution Time)
    @app.after_request
    def after_request_hook(response):
        if hasattr(request, 'start_time'):
            duration_ms = round((time.time() - request.start_time) * 1000, 2)
            app.logger.info(f"{request.method} {request.path} -> Status {response.status_code} ({duration_ms} ms)")
        return response

    # Health Check Endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "environment": config_name,
            "database": "connected"
        }), 200

    # Root API Endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            "name": "Employee REST API",
            "version": "1.0.0",
            "description": "PY-ADV-08 — REST API Development Fundamentals Project",
            "endpoints": {
                "health": "/health",
                "employees": "/employees"
            }
        }), 200

    # Create Database Tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
