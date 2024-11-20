from app.app_main import db
from werkzeug.security import generate_password_hash,check_password_hash


class Admins(db.Model):
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Serial (Auto-Increment)
    adminName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(15), unique=True, nullable=False)  # Assuming phone numbers are unique

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'admin_id': self.admin_id,
            'adminName': self.adminName,
            'email': self.email,
            'phoneNumber': self.phoneNumber
        }
    
    def set_password(self, password):
        """Hash the password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Admin {self.adminName}>'


