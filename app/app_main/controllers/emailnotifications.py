from flask import request
from flask_restx import Resource
from app.app_main.controllers.email_utils import send_email
from app.app_main.dto.emailnotifications import EmailnotificationsDto


requestaccepted_blueprint=EmailnotificationsDto.requestaccepted
@requestaccepted_blueprint.route('/notify', methods=['POST'])
class RequestAcceptedNotification(Resource):
    def post(self):
        """
        Endpoint to send a 'Request Accepted' email.
        The email content can be customized further with dynamic data.
        """
        data = request.json
        email = data.get('email')
        booking_id = data.get('booking_id') 
        if not email:
            return {"error": "Email is required"}, 400

        subject = f"Your Service Request (Booking ID: {booking_id}) has been Accepted"
        template = f"""
            <h1>Request Accepted</h1>
            <p>Your service request with Booking ID: <strong>{booking_id}</strong> has been accepted.</p>
        """
        
        send_email(email, subject, template)  
        return {"message": "Request accepted email sent."},202

driverassigned_blueprint = EmailnotificationsDto.driverassigned
@driverassigned_blueprint.route('/notify', methods=['POST'])
class DriverAssignedNotification(Resource):
    def post(self):
        """
        Endpoint to send a 'Driver Assigned' email.
        This endpoint sends a notification email to the user when a driver is assigned to their service request.
        """
        data = request.json  
        email = data.get('email') 
        driver_name = data.get('driver_name')  
        booking_id = data.get('booking_id')  

        if not email or not driver_name or not booking_id:
            return {"error": "Email, driver_name, and booking_id are required"}, 400

        subject = f"Driver Assigned for Booking ID: {booking_id}"
        template = f"""
            <h1>Driver Assigned</h1>
            <p>Your service request (Booking ID: {booking_id}) has been assigned to a driver.</p>
            <p>Driver Name: {driver_name}</p>
            <p>We will notify you with further details once the service is underway.</p>
        """

        send_email(email, subject, template)

        return {"message": f"Driver assigned email sent to {email}."},202

servicecompleted_blueprint=EmailnotificationsDto.servicecompleted
@servicecompleted_blueprint.route('/notify', methods=['POST'])
class ServiceCompletedNotification(Resource):
    def post(self):
        """
        Endpoint to send a 'Service Completed' email.
        """
        data = request.json
        email = data.get('email') 
        if not email:
            return {"error": "Email is required"}, 400

        subject = "Service Completed"
        template = "<h1>Service Completed</h1><p>Your service has been completed.</p>"
        
        send_email(email, subject, template)  
        return {"message": "Service completion email sent."},202

billinginvoice_blueprint=EmailnotificationsDto.billinginvoice
@billinginvoice_blueprint.route('/notify', methods=['POST'])
class BillingInvoiceNotification(Resource):
    def post(self):
        """
        Endpoint to send a 'Billing Invoice' email.
        """
        data = request.json
        email = data.get('email')
        if not email:
            return {"error": "Email is required"}, 400

        subject = "Billing Invoice"
        template = "<h1>Billing Invoice</h1><p>Your billing invoice is attached.</p>"
        
        send_email(email, subject, template) 
        return {"message": "Billing invoice email sent."},202
