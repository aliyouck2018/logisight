"""Alert model."""

from app import db
from app.models.base import BaseModel


class Alert(BaseModel):
    """Alert model for tracking system alerts."""
    
    alert_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    alert_type = db.Column(db.String(50), nullable=False)  # delay, customs_hold, low_inventory, temperature, etc.
    severity = db.Column(db.String(20), default='medium', nullable=False)  # low, medium, high, critical
    related_entity = db.Column(db.String(100), nullable=False)  # shipment, warehouse, inventory
    related_entity_id = db.Column(db.String(50), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='active', nullable=False)  # active, resolved, acknowledged
    triggered_at = db.Column(db.DateTime, nullable=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    action_taken = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'alert_id': self.alert_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'related_entity': self.related_entity,
            'related_entity_id': self.related_entity_id,
            'message': self.message,
            'status': self.status,
            'triggered_at': self.triggered_at.isoformat() if self.triggered_at else None,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'action_taken': self.action_taken,
            'notes': self.notes,
        })
        return data
