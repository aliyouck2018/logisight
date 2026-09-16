"""Inventory routes."""

from flask import Blueprint, request, jsonify
from app.models.inventory import Inventory
from app import db
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@bp.route('', methods=['GET'])
def get_inventory():
    """Get all inventory items with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    category = request.args.get('category', None, type=str)
    supplier = request.args.get('supplier', None, type=str)
    low_stock = request.args.get('low_stock', 'false', type=str).lower() == 'true'
    
    query = Inventory.query
    
    if category:
        query = query.filter_by(category=category)
    if supplier:
        query = query.filter_by(supplier=supplier)
    if low_stock:
        query = query.filter(Inventory.quantity <= Inventory.reorder_level)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<sku>', methods=['GET'])
def get_item(sku):
    """Get a specific inventory item by SKU."""
    item = Inventory.query.filter_by(sku=sku).first()
    
    if not item:
        return jsonify({
            'success': False,
            'error': 'Inventory item not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': item.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_item():
    """Create a new inventory item."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['sku', 'product_name', 'unit']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate SKU
    if Inventory.query.filter_by(sku=data['sku']).first():
        return jsonify({
            'success': False,
            'error': 'SKU already exists'
        }), 409
    
    item = Inventory(
        sku=data['sku'],
        product_name=data['product_name'],
        description=data.get('description'),
        category=data.get('category'),
        quantity=data.get('quantity', 0),
        unit=data['unit'],
        reorder_level=data.get('reorder_level'),
        reorder_quantity=data.get('reorder_quantity'),
        unit_cost=data.get('unit_cost'),
        cost_currency=data.get('cost_currency', 'USD'),
        supplier=data.get('supplier'),
        last_restocked=datetime.fromisoformat(data['last_restocked']) if data.get('last_restocked') else None,
        expiration_date=datetime.fromisoformat(data['expiration_date']) if data.get('expiration_date') else None,
        notes=data.get('notes')
    )
    
    item.save()
    
    return jsonify({
        'success': True,
        'data': item.to_dict(),
        'message': 'Inventory item created successfully'
    }), 201


@bp.route('/<sku>', methods=['PUT'])
def update_item(sku):
    """Update an inventory item."""
    item = Inventory.query.filter_by(sku=sku).first()
    
    if not item:
        return jsonify({
            'success': False,
            'error': 'Inventory item not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'product_name' in data:
        item.product_name = data['product_name']
    if 'description' in data:
        item.description = data['description']
    if 'category' in data:
        item.category = data['category']
    if 'quantity' in data:
        item.quantity = data['quantity']
    if 'unit' in data:
        item.unit = data['unit']
    if 'reorder_level' in data:
        item.reorder_level = data['reorder_level']
    if 'reorder_quantity' in data:
        item.reorder_quantity = data['reorder_quantity']
    if 'unit_cost' in data:
        item.unit_cost = data['unit_cost']
    if 'cost_currency' in data:
        item.cost_currency = data['cost_currency']
    if 'supplier' in data:
        item.supplier = data['supplier']
    if 'last_restocked' in data:
        item.last_restocked = datetime.fromisoformat(data['last_restocked']) if data['last_restocked'] else None
    if 'expiration_date' in data:
        item.expiration_date = datetime.fromisoformat(data['expiration_date']) if data['expiration_date'] else None
    if 'notes' in data:
        item.notes = data['notes']
    
    item.save()
    
    return jsonify({
        'success': True,
        'data': item.to_dict(),
        'message': 'Inventory item updated successfully'
    }), 200


@bp.route('/<sku>', methods=['DELETE'])
def delete_item(sku):
    """Delete an inventory item."""
    item = Inventory.query.filter_by(sku=sku).first()
    
    if not item:
        return jsonify({
            'success': False,
            'error': 'Inventory item not found'
        }), 404
    
    item.delete()
    
    return jsonify({
        'success': True,
        'message': 'Inventory item deleted successfully'
    }), 200
