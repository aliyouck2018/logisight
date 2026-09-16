"""Customs routes (placeholder for Phase 4)."""

from flask import Blueprint

bp = Blueprint('customs', __name__, url_prefix='/customs')


@bp.route('', methods=['GET'])
def index():
    """Customs analytics."""
    return {'message': 'Customs Analytics - Coming in Phase 6'}, 200
