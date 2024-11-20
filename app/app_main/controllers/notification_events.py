from app.app_main.controllers.notifications import notify_user  # Import the notify_user function

def on_request_confirmed(user_id,booking_id):
    """Notify user when their request is confirmed."""
    notify_user("request_confirmed", "Your request has been confirmed.", user_id,booking_id)

def on_driver_assigned(user_id,booking_id):
    """Notify user when a driver is assigned to their request."""
    notify_user("driver_assigned", "A driver has been assigned to your request.", user_id,booking_id)

def on_enroute_for_pickup(user_id,booking_id):
    """Notify user when the driver is enroute for pickup."""
    notify_user("enroute_for_pickup", "The driver is enroute for pickup.", user_id,booking_id)

def on_vehicle_picked_up(user_id,booking_id):
    """Notify user when their vehicle has been picked up by the driver."""
    notify_user("vehicle_picked_up", "Your vehicle has been picked up by the driver.", user_id,booking_id)

def on_vehicle_servicing_pending(user_id,booking_id):
    """Notify user when their vehicle servicing is pending."""
    notify_user("vehicle_servicing_pending", "Your vehicle servicing is pending.", user_id,booking_id)

def on_vehicle_servicing_completed(user_id,booking_id):
    """Notify user when their vehicle servicing is completed."""
    notify_user("vehicle_servicing_completed", "Your vehicle servicing is completed.", user_id,booking_id)

def on_enroute_for_dropoff(user_id,booking_id):
    """Notify user when the driver is enroute for dropoff."""
    notify_user("enroute_for_dropoff", "The driver is enroute for dropoff.", user_id,booking_id)

def on_vehicle_dropped_off(user_id,booking_id):
    """Notify user when their vehicle has been dropped off successfully."""
    notify_user("vehicle_dropped_off", "Your vehicle has been dropped off successfully.", user_id,booking_id)
