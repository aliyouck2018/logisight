"""Warehouse model."""

from app import db
from app.models.base import BaseModel


class Warehouse(BaseModel):
    """Warehouse model for tracking warehouse locations and inventory."""
    
    warehouse_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    capacity = db.Column(db.Float, nullable=True)  # in cubic meters
    current_occupancy = db.Column(db.Float, default=0, nullable=False)  # in cubic meters
    manager_name = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    operational_status = db.Column(db.String(50), default='operational', nullable=False)  # operational, maintenance, closed
    storage_types = db.Column(db.String(500), nullable=True)  # comma-separated: climate_controlled, refrigerated, secure, etc.
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'warehouse_id': self.warehouse_id,
            'name': self.name,
            'location': self.location,
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'capacity': self.capacity,
            'current_occupancy': self.current_occupancy,
            'occupancy_percentage': (self.current_occupancy / self.capacity * 100) if self.capacity else 0,
            'manager_name': self.manager_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'operational_status': self.operational_status,
            'storage_types': self.storage_types,
            'notes': self.notes,
        })
        return data
