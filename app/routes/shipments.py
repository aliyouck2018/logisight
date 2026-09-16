"""Shipments routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('shipments', __name__, url_prefix='/shipments')


@bp.route('', methods=['GET'])
def list_shipments():
    """List shipments."""
    return {'message': 'Shipments - Coming in Phase 6'}, 200
