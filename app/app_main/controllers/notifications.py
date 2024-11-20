from app.app_main import socketio
from flask_socketio import emit
from app.app_main import db
from flask_restx import Resource
from app.app_main.models import Notifications,ServiceBookings
from app.app_main.dto.notifications import NotificationsDto

# Function to emit notification event to a specific user
def notify_user(event_type, message, user_id,booking_id):
    notification_data = {
        'type': event_type,
        'message': message,
        'user_id': user_id,
        'booking_id':booking_id
    }
    # Emit the notification event to a specific user (using `user_id` as room)
    socketio.emit('notification', notification_data, room=user_id)

    # Optional: Store the notification in the database (if you want to persist them)
    notification = Notifications(user_id=user_id, type=event_type, message=message,booking_id=booking_id,is_read=False)
    db.session.add(notification)
    db.session.commit()

getnotifications_blueprint= NotificationsDto.getnotifications
@getnotifications_blueprint.route('/<user_id>',methods=['GET'])
class GetNotifications(Resource):
    def get(self, user_id):
        # Query Notifications table directly with the given user_id and sort by created_at
        notifications_query = db.session.query(Notifications).filter(
            Notifications.user_id == user_id
        ).order_by(Notifications.created_at.desc()).all()


        if not notifications_query:
            return {'message': 'No notifications found for this user.'}, 404

        # Prepare the response data in the requested format
        combined_results = [
            {
                'n_id': str(notification.n_id),
                'message': notification.message,
                'is_read': notification.is_read,
                'user_id': str(notification.user_id),
                'booking_id': str(notification.booking_id) if notification.booking_id else None,
                'created_at': notification.created_at.isoformat()  # Ensure date is in ISO format
            }
            for notification in notifications_query
        ]

        # Return the combined array of notifications
        return {'notifications': combined_results}

    
updatenotification_blueprint= NotificationsDto.updatenotification
@updatenotification_blueprint.route('/<string:n_id>',methods=['PUT'])
class UpdateNotification(Resource):
    def put(self, n_id):
        # Find the specific notification by its ID
        notification = Notifications.query.get(n_id)

        if not notification:
            return {'message': 'No notification found.'}, 404

        try:
             notification.mark_as_read()
        except Exception as e:
            db.session.rollback()

            return {'message': f'Error updating notification: {str(e)}'}, 500
        
        return {'message': 'Notification marked as read successfully', 'notification': notification.to_dict()}, 200


deletenotification_blueprint=NotificationsDto.deletenotifications
@deletenotification_blueprint.route('/<n_id>', methods=['DELETE'])
class DeleteNotification(Resource):
    def delete(self, n_id):
        # Find the notification by its ID
        notification = Notifications.query.get(n_id)
        
        if notification is None:
            # Return a 404 if the notification is not found
            return {'error': 'Notification not found'}, 404
        
        # Delete the notification from the database
        db.session.delete(notification)
        db.session.commit()
        
        # Return a success response
        return {'message': 'Notification deleted successfully'}, 200