from flask_socketio import emit
from app.app_main import socketio  # Import the `socketio` instance
from app.app_main.controllers.notification_events import (on_request_confirmed,on_driver_assigned,on_enroute_for_pickup,
on_vehicle_picked_up,on_vehicle_servicing_pending,on_vehicle_servicing_completed,on_enroute_for_dropoff,on_vehicle_dropped_off)
# Map event types to corresponding functions
NOTIFICATION_EVENTS = {
    "request_confirmed": on_request_confirmed,
    "driver_assigned": on_driver_assigned,
    "enroute_for_pickup": on_enroute_for_pickup,
    "vehicle_picked_up": on_vehicle_picked_up,
    "vehicle_servicing_pending": on_vehicle_servicing_pending,
    "vehicle_servicing_completed": on_vehicle_servicing_completed,
    "enroute_for_dropoff": on_enroute_for_dropoff,
    "vehicle_dropped_off": on_vehicle_dropped_off
}


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'message': 'Connected to WebSocket server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('update_status')
def handle_status_update(data):
    print('Status update received:', data)
    emit('status_update', data, broadcast=True)

@socketio.on('trigger_notification')
def handle_trigger_notification(data):
    # Example: { "event_type": "info", "user_id": "1234" }
    print(f"Received notification event: {data}") 
    event_type = data.get("event_type")
    user_id = data.get("user_id")
    booking_id=data.get("booking_id")
     # Check if the event type has a corresponding function
    notification_function = NOTIFICATION_EVENTS.get(event_type)
    
    if notification_function and user_id and booking_id:
        # Call the appropriate notification function
        notification_function(user_id,booking_id)
    else:
        print(f"Unrecognized event type: {event_type} or missing user_id.")
