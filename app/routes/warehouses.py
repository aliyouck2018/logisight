"""Warehouse routes."""

from flask import Blueprint, request, jsonify
from app.models.warehouse import Warehouse
from app import db

bp = Blueprint('warehouses', __name__, url_prefix='/api/warehouses')


@bp.route('', methods=['GET'])
def get_warehouses():
    """Get all warehouses with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status', None, type=str)
    country = request.args.get('country', None, type=str)
    
    query = Warehouse.query
    
    if status:
        query = query.filter_by(operational_status=status)
    if country:
        query = query.filter_by(country=country)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [warehouse.to_dict() for warehouse in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    """Get a specific warehouse by ID."""
    warehouse = Warehouse.query.filter_by(warehouse_id=warehouse_id).first()
    
    if not warehouse:
        return jsonify({
            'success': False,
            'error': 'Warehouse not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': warehouse.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_warehouse():
    """Create a new warehouse."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['warehouse_id', 'name', 'location', 'city', 'country']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate warehouse_id
    if Warehouse.query.filter_by(warehouse_id=data['warehouse_id']).first():
        return jsonify({
            'success': False,
            'error': 'Warehouse ID already exists'
        }), 409
    
    warehouse = Warehouse(
        warehouse_id=data['warehouse_id'],
        name=data['name'],
        location=data['location'],
        city=data['city'],
        country=data['country'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        capacity=data.get('capacity'),
        current_occupancy=data.get('current_occupancy', 0),
        manager_name=data.get('manager_name'),
        contact_email=data.get('contact_email'),
        contact_phone=data.get('contact_phone'),
        operational_status=data.get('operational_status', 'operational'),
        storage_types=data.get('storage_types'),
        notes=data.get('notes')
    )
    
    warehouse.save()
    
    return jsonify({
        'success': True,
        'data': warehouse.to_dict(),
        'message': 'Warehouse created successfully'
    }), 201


@bp.route('/<warehouse_id>', methods=['PUT'])
def update_warehouse(warehouse_id):
    """Update a warehouse."""
    warehouse = Warehouse.query.filter_by(warehouse_id=warehouse_id).first()
    
    if not warehouse:
        return jsonify({
            'success': False,
            'error': 'Warehouse not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'name' in data:
        warehouse.name = data['name']
    if 'location' in data:
        warehouse.location = data['location']
    if 'city' in data:
        warehouse.city = data['city']
    if 'country' in data:
        warehouse.country = data['country']
    if 'latitude' in data:
        warehouse.latitude = data['latitude']
    if 'longitude' in data:
        warehouse.longitude = data['longitude']
    if 'capacity' in data:
        warehouse.capacity = data['capacity']
    if 'current_occupancy' in data:
        warehouse.current_occupancy = data['current_occupancy']
    if 'manager_name' in data:
        warehouse.manager_name = data['manager_name']
    if 'contact_email' in data:
        warehouse.contact_email = data['contact_email']
    if 'contact_phone' in data:
        warehouse.contact_phone = data['contact_phone']
    if 'operational_status' in data:
        warehouse.operational_status = data['operational_status']
    if 'storage_types' in data:
        warehouse.storage_types = data['storage_types']
    if 'notes' in data:
        warehouse.notes = data['notes']
    
    warehouse.save()
    
    return jsonify({
        'success': True,
        'data': warehouse.to_dict(),
        'message': 'Warehouse updated successfully'
    }), 200


@bp.route('/<warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    warehouse = Warehouse.query.filter_by(warehouse_id=warehouse_id).first()
    
    if not warehouse:
        return jsonify({
            'success': False,
            'error': 'Warehouse not found'
        }), 404
    
    warehouse.delete()
    
    return jsonify({
        'success': True,
        'message': 'Warehouse deleted successfully'
    }), 200
