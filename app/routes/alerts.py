"""Alert routes."""

from flask import Blueprint, request, jsonify
from app.models.alert import Alert
from app import db
from datetime import datetime

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')


@bp.route('', methods=['GET'])
def get_alerts():
    """Get all alerts with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status', None, type=str)
    severity = request.args.get('severity', None, type=str)
    alert_type = request.args.get('alert_type', None, type=str)
    
    query = Alert.query
    
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    if alert_type:
        query = query.filter_by(alert_type=alert_type)
    
    # Order by triggered_at descending (most recent first)
    query = query.order_by(Alert.triggered_at.desc())
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [alert.to_dict() for alert in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200


@bp.route('/<alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get a specific alert by ID."""
    alert = Alert.query.filter_by(alert_id=alert_id).first()
    
    if not alert:
        return jsonify({
            'success': False,
            'error': 'Alert not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': alert.to_dict()
    }), 200


@bp.route('', methods=['POST'])
def create_alert():
    """Create a new alert."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['alert_id', 'alert_type', 'related_entity', 'related_entity_id', 'message']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {missing_fields}'
        }), 400
    
    # Check for duplicate alert_id
    if Alert.query.filter_by(alert_id=data['alert_id']).first():
        return jsonify({
            'success': False,
            'error': 'Alert ID already exists'
        }), 409
    
    alert = Alert(
        alert_id=data['alert_id'],
        alert_type=data['alert_type'],
        severity=data.get('severity', 'medium'),
        related_entity=data['related_entity'],
        related_entity_id=data['related_entity_id'],
        message=data['message'],
        status=data.get('status', 'active'),
        triggered_at=datetime.fromisoformat(data['triggered_at']) if data.get('triggered_at') else datetime.utcnow(),
        acknowledged_at=datetime.fromisoformat(data['acknowledged_at']) if data.get('acknowledged_at') else None,
        resolved_at=datetime.fromisoformat(data['resolved_at']) if data.get('resolved_at') else None,
        action_taken=data.get('action_taken'),
        notes=data.get('notes')
    )
    
    alert.save()
    
    return jsonify({
        'success': True,
        'data': alert.to_dict(),
        'message': 'Alert created successfully'
    }), 201


@bp.route('/<alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update an alert."""
    alert = Alert.query.filter_by(alert_id=alert_id).first()
    
    if not alert:
        return jsonify({
            'success': False,
            'error': 'Alert not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields
    if 'status' in data:
        alert.status = data['status']
    if 'severity' in data:
        alert.severity = data['severity']
    if 'message' in data:
        alert.message = data['message']
    if 'acknowledged_at' in data:
        alert.acknowledged_at = datetime.fromisoformat(data['acknowledged_at']) if data['acknowledged_at'] else None
    if 'resolved_at' in data:
        alert.resolved_at = datetime.fromisoformat(data['resolved_at']) if data['resolved_at'] else None
    if 'action_taken' in data:
        alert.action_taken = data['action_taken']
    if 'notes' in data:
        alert.notes = data['notes']
    
    alert.save()
    
    return jsonify({
        'success': True,
        'data': alert.to_dict(),
        'message': 'Alert updated successfully'
    }), 200


@bp.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete an alert."""
    alert = Alert.query.filter_by(alert_id=alert_id).first()
    
    if not alert:
        return jsonify({
            'success': False,
            'error': 'Alert not found'
        }), 404
    
    alert.delete()
    
    return jsonify({
        'success': True,
        'message': 'Alert deleted successfully'
    }), 200
