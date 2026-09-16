"""Reports routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('', methods=['GET'])
def index():
    """Reports."""
    return {'message': 'Reports - Coming in Phase 6'}, 200
