"""Alerts routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('alerts', __name__, url_prefix='/alerts')


@bp.route('', methods=['GET'])
def index():
    """Alerts."""
    return {'message': 'Alerts - Coming in Phase 6'}, 200
