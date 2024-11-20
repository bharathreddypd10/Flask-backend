from app.app_main import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class Notifications(db.Model):
    __tablename__ = 'notifications'
    n_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    booking_id = db.Column(UUID(as_uuid=True), db.ForeignKey('servicebookings.booking_id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)  
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('Users', backref='notifications', lazy=True)
    servicebooking = db.relationship('ServiceBookings', backref='notifications', lazy=True)

    def __repr__(self):
        return f'<Notification {self.n_id} for User {self.user_id}>'

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'n_id': str(self.n_id),
            'user_id': str(self.user_id),
            'booking_id': str(self.booking_id),
            'type': self.type,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'is_read': self.is_read
        }

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        db.session.commit()