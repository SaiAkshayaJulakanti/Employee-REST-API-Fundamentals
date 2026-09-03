"""
Application Entry Point for Employee REST API.
"""
import os
from app import create_app

env = os.environ.get('FLASK_ENV', 'dev')
app = create_app(env)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Employee REST API server on http://127.0.0.1:{port} (Env: {env})")
    app.run(host='0.0.0.0', port=port, debug=True)
