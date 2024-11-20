import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.app_main import db


class ServiceBookings(db.Model):
    __tablename__ = 'servicebookings'

    booking_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID as Primary Key
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    driver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('drivers.driver_id'), nullable=True)
    vehicle_type = db.Column(db.String(50), nullable=False)  # E.g., Car, Bike, Truck
    vehicle_number = db.Column(db.String(20), nullable=False)  # License plate number
    service_type = db.Column(db.String(100), nullable=False)  # E.g., Maintenance, Repair
    preferred_date = db.Column(db.Date, nullable=False)  # Preferred service date
    preferred_time = db.Column(db.Time, nullable=False)  # Preferred service time
    pickup_location = db.Column(db.String(200), nullable=False)  # Address or pickup location
    status = db.Column(db.String(50), default='pending')  # Status of the booking (e.g., pending, accepted, completed)

    user = db.relationship('Users', backref='servicebookings', lazy=True)
    driver = db.relationship('Drivers', backref='assigned_bookings', lazy=True)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'booking_id': str(self.booking_id),  # UUIDs need to be cast to strings
            'vehicle_type': self.vehicle_type,
            'driver_id': str(self.driver_id) if self.driver_id else None,
            'vehicle_number': self.vehicle_number,
            'service_type': self.service_type,
            'preferred_date': self.preferred_date.strftime('%Y-%m-%d'),  # Format date
            'preferred_time': self.preferred_time.strftime('%H:%M:%S'),  # Format time
            'pickup_location': self.pickup_location,
            'status': self.status
        }