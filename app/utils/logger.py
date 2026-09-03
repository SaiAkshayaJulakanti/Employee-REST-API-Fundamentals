"""
Structured Logger Setup Module for Flask Application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """
    Configure application logging to write logs to both stdout console
    and rotating file `logs/app.log`.
    """
    log_dir = app.config.get('LOG_DIR', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = app.config.get('LOG_FILE', os.path.join(log_dir, 'app.log'))

    # Formatter definition
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s'
    )

    # File Handler (Max 5MB per log file, keeping up to 3 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Clear pre-existing handlers to prevent duplicate output
    app.logger.handlers.clear()
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    app.logger.info("Application logger initialized successfully.")
