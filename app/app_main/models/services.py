from app.app_main import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Services(db.Model):
    __tablename__ = 'services'

    service_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID as Primary Key
    service_type = db.Column(db.String(50), nullable=False)  # Type of service (e.g., Maintenance, Repair)
    price = db.Column(db.Float, nullable=False)  # Service price

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'service_id': str(self.service_id),  # UUIDs need to be cast to strings
            'service_type': self.service_type,
            'price': self.price
        }
