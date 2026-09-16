"""Shipment routes."""

from flask import Blueprint, request, jsonify
from app.models.shipment import Shipment
from app import db
from datetime import datetime

bp = Blueprint('shipments', __name__, url_prefix='/api/shipments')


@bp.route('', methods=['GET'])
def get_shipments():
    """Get all shipments with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status', None, type=str)
    
    query = Shipment.query
    
    if status:
        query = query.filter_by(status=status)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [shipment.to_dict() for shipment in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    """Get a specific shipment by ID."""
    shipment = Shipment.query.filter_by(shipment_id=shipment_id).first()
    
    if not shipment:
        return jsonify({
            'success': False,
            'error': 'Shipment not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': shipment.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_shipment():
    """Create a new shipment."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['shipment_id', 'origin', 'destination']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate shipment_id
    if Shipment.query.filter_by(shipment_id=data['shipment_id']).first():
        return jsonify({
            'success': False,
            'error': 'Shipment ID already exists'
        }), 409
    
    shipment = Shipment(
        shipment_id=data['shipment_id'],
        origin=data['origin'],
        destination=data['destination'],
        status=data.get('status', 'pending'),
        weight=data.get('weight'),
        value=data.get('value'),
        carrier=data.get('carrier'),
        tracking_number=data.get('tracking_number'),
        departure_date=datetime.fromisoformat(data['departure_date']) if data.get('departure_date') else None,
        arrival_date=datetime.fromisoformat(data['arrival_date']) if data.get('arrival_date') else None,
        notes=data.get('notes')
    )
    
    shipment.save()
    
    return jsonify({
        'success': True,
        'data': shipment.to_dict(),
        'message': 'Shipment created successfully'
    }), 201


@bp.route('/<shipment_id>', methods=['PUT'])
def update_shipment(shipment_id):
    """Update a shipment."""
    shipment = Shipment.query.filter_by(shipment_id=shipment_id).first()
    
    if not shipment:
        return jsonify({
            'success': False,
            'error': 'Shipment not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'origin' in data:
        shipment.origin = data['origin']
    if 'destination' in data:
        shipment.destination = data['destination']
    if 'status' in data:
        shipment.status = data['status']
    if 'weight' in data:
        shipment.weight = data['weight']
    if 'value' in data:
        shipment.value = data['value']
    if 'carrier' in data:
        shipment.carrier = data['carrier']
    if 'tracking_number' in data:
        shipment.tracking_number = data['tracking_number']
    if 'departure_date' in data:
        shipment.departure_date = datetime.fromisoformat(data['departure_date']) if data['departure_date'] else None
    if 'arrival_date' in data:
        shipment.arrival_date = datetime.fromisoformat(data['arrival_date']) if data['arrival_date'] else None
    if 'notes' in data:
        shipment.notes = data['notes']
    
    shipment.save()
    
    return jsonify({
        'success': True,
        'data': shipment.to_dict(),
        'message': 'Shipment updated successfully'
    }), 200


@bp.route('/<shipment_id>', methods=['DELETE'])
def delete_shipment(shipment_id):
    """Delete a shipment."""
    shipment = Shipment.query.filter_by(shipment_id=shipment_id).first()
    
    if not shipment:
        return jsonify({
            'success': False,
            'error': 'Shipment not found'
        }), 404
    
    shipment.delete()
    
    return jsonify({
        'success': True,
        'message': 'Shipment deleted successfully'
    }), 200
