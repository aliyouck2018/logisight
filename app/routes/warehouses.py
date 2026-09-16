"""Warehouse routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('warehouses', __name__, url_prefix='/warehouses')


@bp.route('', methods=['GET'])
def index():
    """Warehouse analytics."""
    return {'message': 'Warehouse Analytics - Coming in Phase 6'}, 200
