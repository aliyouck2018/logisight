"""Health check routes."""

from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint.
    
    Returns:
        JSON response indicating application health
    """
    return jsonify({
        'status': 'ok',
        'message': 'LogiSight API is running'
    }), 200
