"""Customs Declaration routes."""

from flask import Blueprint, request, jsonify
from app.models.customs_declaration import CustomsDeclaration
from app import db
from datetime import datetime

bp = Blueprint('customs', __name__, url_prefix='/api/customs')


@bp.route('', methods=['GET'])
def get_declarations():
    """Get all customs declarations with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status', None, type=str)
    shipment_id = request.args.get('shipment_id', None, type=str)
    
    query = CustomsDeclaration.query
    
    if status:
        query = query.filter_by(status=status)
    if shipment_id:
        query = query.filter_by(shipment_id=shipment_id)
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [decl.to_dict() for decl in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<declaration_id>', methods=['GET'])
def get_declaration(declaration_id):
    """Get a specific customs declaration by ID."""
    declaration = CustomsDeclaration.query.filter_by(declaration_id=declaration_id).first()
    
    if not declaration:
        return jsonify({
            'success': False,
            'error': 'Customs declaration not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': declaration.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_declaration():
    """Create a new customs declaration."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['declaration_id', 'shipment_id', 'hs_code', 'description', 
                      'quantity', 'unit', 'declared_value', 'country_of_origin']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate declaration_id
    if CustomsDeclaration.query.filter_by(declaration_id=data['declaration_id']).first():
        return jsonify({
            'success': False,
            'error': 'Declaration ID already exists'
        }), 409
    
    declaration = CustomsDeclaration(
        declaration_id=data['declaration_id'],
        shipment_id=data['shipment_id'],
        hs_code=data['hs_code'],
        description=data['description'],
        quantity=data['quantity'],
        unit=data['unit'],
        declared_value=data['declared_value'],
        currency=data.get('currency', 'USD'),
        country_of_origin=data['country_of_origin'],
        status=data.get('status', 'pending'),
        declaration_date=datetime.fromisoformat(data['declaration_date']) if data.get('declaration_date') else datetime.utcnow(),
        approval_date=datetime.fromisoformat(data['approval_date']) if data.get('approval_date') else None,
        notes=data.get('notes')
    )
    
    declaration.save()
    
    return jsonify({
        'success': True,
        'data': declaration.to_dict(),
        'message': 'Customs declaration created successfully'
    }), 201


@bp.route('/<declaration_id>', methods=['PUT'])
def update_declaration(declaration_id):
    """Update a customs declaration."""
    declaration = CustomsDeclaration.query.filter_by(declaration_id=declaration_id).first()
    
    if not declaration:
        return jsonify({
            'success': False,
            'error': 'Customs declaration not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'hs_code' in data:
        declaration.hs_code = data['hs_code']
    if 'description' in data:
        declaration.description = data['description']
    if 'quantity' in data:
        declaration.quantity = data['quantity']
    if 'unit' in data:
        declaration.unit = data['unit']
    if 'declared_value' in data:
        declaration.declared_value = data['declared_value']
    if 'currency' in data:
        declaration.currency = data['currency']
    if 'country_of_origin' in data:
        declaration.country_of_origin = data['country_of_origin']
    if 'status' in data:
        declaration.status = data['status']
    if 'approval_date' in data:
        declaration.approval_date = datetime.fromisoformat(data['approval_date']) if data['approval_date'] else None
    if 'notes' in data:
        declaration.notes = data['notes']
    
    declaration.save()
    
    return jsonify({
        'success': True,
        'data': declaration.to_dict(),
        'message': 'Customs declaration updated successfully'
    }), 200


@bp.route('/<declaration_id>', methods=['DELETE'])
def delete_declaration(declaration_id):
    """Delete a customs declaration."""
    declaration = CustomsDeclaration.query.filter_by(declaration_id=declaration_id).first()
    
    if not declaration:
        return jsonify({
            'success': False,
            'error': 'Customs declaration not found'
        }), 404
    
    declaration.delete()
    
    return jsonify({
        'success': True,
        'message': 'Customs declaration deleted successfully'
    }), 200
