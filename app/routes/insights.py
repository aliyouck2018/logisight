"""Insights routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('insights', __name__, url_prefix='/insights')


@bp.route('', methods=['GET'])
def index():
    """Insights."""
    return {'message': 'Insights - Coming in Phase 6'}, 200
