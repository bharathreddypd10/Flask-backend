import uuid
from app.app_main import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

class Drivers(db.Model):
    __tablename__ = 'drivers'
    
    driver_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_name = db.Column(db.String(80), nullable=False)
    driver_age = db.Column(db.Integer, nullable=False)
    driver_email = db.Column(db.String(120), unique=True, nullable=False)
    driver_mobile = db.Column(db.String(15), unique=True, nullable=False)
    driver_password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='free') 

    def __repr__(self):
        return f'<Driver {self.driver_name}>'

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'driver_id': str(self.driver_id),
            'driver_name': self.driver_name,
            'driver_age': self.driver_age,
            'driver_email': self.driver_email,
            'driver_mobile': self.driver_mobile,
            'status': self.status
        }

    def set_password(self, password):
        self.driver_password = generate_password_hash(password, salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.driver_password, password)