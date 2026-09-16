"""WarehouseInventory association model."""

from app import db
from app.models.base import BaseModel


class WarehouseInventory(BaseModel):
    """WarehouseInventory model linking warehouses and inventory items."""
    
    warehouse_id = db.Column(db.String(50), db.ForeignKey('warehouse.warehouse_id'), nullable=False, index=True)
    inventory_sku = db.Column(db.String(50), db.ForeignKey('inventory.sku'), nullable=False, index=True)
    quantity_on_hand = db.Column(db.Float, default=0, nullable=False)
    quantity_reserved = db.Column(db.Float, default=0, nullable=False)
    quantity_available = db.Column(db.Float, default=0, nullable=False)
    location_code = db.Column(db.String(100), nullable=True)  # Shelf/Bin location
    last_counted = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('warehouse_id', 'inventory_sku', name='unique_warehouse_inventory'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'warehouse_id': self.warehouse_id,
            'inventory_sku': self.inventory_sku,
            'quantity_on_hand': self.quantity_on_hand,
            'quantity_reserved': self.quantity_reserved,
            'quantity_available': self.quantity_available,
            'location_code': self.location_code,
            'last_counted': self.last_counted.isoformat() if self.last_counted else None,
            'notes': self.notes,
        })
        return data
