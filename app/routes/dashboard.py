"""Dashboard routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('', methods=['GET'])
def index():
    """Dashboard home page."""
    return {'message': 'Dashboard - Coming in Phase 6'}, 200
