"""Transport Route endpoints."""

from flask import Blueprint, request, jsonify
from app.models.transport_route import TransportRoute
from app import db
from datetime import datetime

bp = Blueprint('transport', __name__, url_prefix='/api/transport')


@bp.route('', methods=['GET'])
def get_routes():
    """Get all transport routes with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status', None, type=str)
    shipment_id = request.args.get('shipment_id', None, type=str)
    transport_mode = request.args.get('transport_mode', None, type=str)
    
    query = TransportRoute.query
    
    if status:
        query = query.filter_by(status=status)
    if shipment_id:
        query = query.filter_by(shipment_id=shipment_id)
    if transport_mode:
        query = query.filter_by(transport_mode=transport_mode)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [route.to_dict() for route in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<route_id>', methods=['GET'])
def get_route(route_id):
    """Get a specific transport route by ID."""
    route = TransportRoute.query.filter_by(route_id=route_id).first()
    
    if not route:
        return jsonify({
            'success': False,
            'error': 'Transport route not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': route.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_route():
    """Create a new transport route."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['route_id', 'shipment_id', 'departure_location', 'arrival_location', 'transport_mode']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate route_id
    if TransportRoute.query.filter_by(route_id=data['route_id']).first():
        return jsonify({
            'success': False,
            'error': 'Route ID already exists'
        }), 409
    
    route = TransportRoute(
        route_id=data['route_id'],
        shipment_id=data['shipment_id'],
        departure_location=data['departure_location'],
        arrival_location=data['arrival_location'],
        transport_mode=data['transport_mode'],
        distance=data.get('distance'),
        estimated_duration=data.get('estimated_duration'),
        actual_duration=data.get('actual_duration'),
        cost=data.get('cost'),
        cost_currency=data.get('cost_currency', 'USD'),
        status=data.get('status', 'pending'),
        scheduled_departure=datetime.fromisoformat(data['scheduled_departure']) if data.get('scheduled_departure') else None,
        actual_departure=datetime.fromisoformat(data['actual_departure']) if data.get('actual_departure') else None,
        scheduled_arrival=datetime.fromisoformat(data['scheduled_arrival']) if data.get('scheduled_arrival') else None,
        actual_arrival=datetime.fromisoformat(data['actual_arrival']) if data.get('actual_arrival') else None,
        carrier_name=data.get('carrier_name'),
        vehicle_id=data.get('vehicle_id'),
        notes=data.get('notes')
    )
    
    route.save()
    
    return jsonify({
        'success': True,
        'data': route.to_dict(),
        'message': 'Transport route created successfully'
    }), 201


@bp.route('/<route_id>', methods=['PUT'])
def update_route(route_id):
    """Update a transport route."""
    route = TransportRoute.query.filter_by(route_id=route_id).first()
    
    if not route:
        return jsonify({
            'success': False,
            'error': 'Transport route not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'departure_location' in data:
        route.departure_location = data['departure_location']
    if 'arrival_location' in data:
        route.arrival_location = data['arrival_location']
    if 'transport_mode' in data:
        route.transport_mode = data['transport_mode']
    if 'distance' in data:
        route.distance = data['distance']
    if 'estimated_duration' in data:
        route.estimated_duration = data['estimated_duration']
    if 'actual_duration' in data:
        route.actual_duration = data['actual_duration']
    if 'cost' in data:
        route.cost = data['cost']
    if 'cost_currency' in data:
        route.cost_currency = data['cost_currency']
    if 'status' in data:
        route.status = data['status']
    if 'scheduled_departure' in data:
        route.scheduled_departure = datetime.fromisoformat(data['scheduled_departure']) if data['scheduled_departure'] else None
    if 'actual_departure' in data:
        route.actual_departure = datetime.fromisoformat(data['actual_departure']) if data['actual_departure'] else None
    if 'scheduled_arrival' in data:
        route.scheduled_arrival = datetime.fromisoformat(data['scheduled_arrival']) if data['scheduled_arrival'] else None
    if 'actual_arrival' in data:
        route.actual_arrival = datetime.fromisoformat(data['actual_arrival']) if data['actual_arrival'] else None
    if 'carrier_name' in data:
        route.carrier_name = data['carrier_name']
    if 'vehicle_id' in data:
        route.vehicle_id = data['vehicle_id']
    if 'notes' in data:
        route.notes = data['notes']
    
    route.save()
    
    return jsonify({
        'success': True,
        'data': route.to_dict(),
        'message': 'Transport route updated successfully'
    }), 200


@bp.route('/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Delete a transport route."""
    route = TransportRoute.query.filter_by(route_id=route_id).first()
    
    if not route:
        return jsonify({
            'success': False,
            'error': 'Transport route not found'
        }), 404
    
    route.delete()
    
    return jsonify({
        'success': True,
        'message': 'Transport route deleted successfully'
    }), 200
