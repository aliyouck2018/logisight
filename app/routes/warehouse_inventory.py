"""Warehouse Inventory routes."""

from flask import Blueprint, request, jsonify
from app.models.warehouse_inventory import WarehouseInventory
from app import db
from datetime import datetime

bp = Blueprint('warehouse_inventory', __name__, url_prefix='/api/warehouse-inventory')


@bp.route('', methods=['GET'])
def get_warehouse_inventory():
    """Get all warehouse inventory with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    warehouse_id = request.args.get('warehouse_id', None, type=str)
    sku = request.args.get('sku', None, type=str)
    
    query = WarehouseInventory.query
    
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)
    if sku:
        query = query.filter_by(inventory_sku=sku)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [wi.to_dict() for wi in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<int:id>', methods=['GET'])
def get_warehouse_inventory_item(id):
    """Get a specific warehouse inventory by ID."""
    wi = WarehouseInventory.query.get(id)
    
    if not wi:
        return jsonify({
            'success': False,
            'error': 'Warehouse inventory not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': wi.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_warehouse_inventory():
    """Create a new warehouse inventory entry."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['warehouse_id', 'inventory_sku']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate warehouse-inventory pair
    existing = WarehouseInventory.query.filter_by(
        warehouse_id=data['warehouse_id'],
        inventory_sku=data['inventory_sku']
    ).first()
    
    if existing:
        return jsonify({
            'success': False,
            'error': 'This warehouse-inventory pair already exists'
        }), 409
    
    wi = WarehouseInventory(
        warehouse_id=data['warehouse_id'],
        inventory_sku=data['inventory_sku'],
        quantity_on_hand=data.get('quantity_on_hand', 0),
        quantity_reserved=data.get('quantity_reserved', 0),
        quantity_available=data.get('quantity_available', 0),
        location_code=data.get('location_code'),
        last_counted=datetime.fromisoformat(data['last_counted']) if data.get('last_counted') else None,
        notes=data.get('notes')
    )
    
    wi.save()
    
    return jsonify({
        'success': True,
        'data': wi.to_dict(),
        'message': 'Warehouse inventory entry created successfully'
    }), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_warehouse_inventory(id):
    """Update a warehouse inventory entry."""
    wi = WarehouseInventory.query.get(id)
    
    if not wi:
        return jsonify({
            'success': False,
            'error': 'Warehouse inventory not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'quantity_on_hand' in data:
        wi.quantity_on_hand = data['quantity_on_hand']
    if 'quantity_reserved' in data:
        wi.quantity_reserved = data['quantity_reserved']
    if 'quantity_available' in data:
        wi.quantity_available = data['quantity_available']
    if 'location_code' in data:
        wi.location_code = data['location_code']
    if 'last_counted' in data:
        wi.last_counted = datetime.fromisoformat(data['last_counted']) if data['last_counted'] else None
    if 'notes' in data:
        wi.notes = data['notes']
    
    wi.save()
    
    return jsonify({
        'success': True,
        'data': wi.to_dict(),
        'message': 'Warehouse inventory entry updated successfully'
    }), 200


@bp.route('/<int:id>', methods=['DELETE'])
def delete_warehouse_inventory(id):
    """Delete a warehouse inventory entry."""
    wi = WarehouseInventory.query.get(id)
    
    if not wi:
        return jsonify({
            'success': False,
            'error': 'Warehouse inventory not found'
        }), 404
    
    wi.delete()
    
    return jsonify({
        'success': True,
        'message': 'Warehouse inventory entry deleted successfully'
    }), 200
