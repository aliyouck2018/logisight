"""Transport routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('transport', __name__, url_prefix='/transport')


@bp.route('', methods=['GET'])
def index():
    """Transport analytics."""
    return {'message': 'Transport Analytics - Coming in Phase 6'}, 200
