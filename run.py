"""Application entry point."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make shell context with app objects."""
    return {'db': db}


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    host = os.getenv('APP_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    app.run(host=host, port=port, debug=debug)
