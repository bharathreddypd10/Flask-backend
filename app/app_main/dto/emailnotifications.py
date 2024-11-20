from flask_restx import Namespace

class EmailnotificationsDto:
    requestaccepted = Namespace('request_accepted',description='api to send email')
    driverassigned = Namespace('driver_assigned',description='api to send email ')
    servicecompleted = Namespace('service_completed',description='api to send email')
    billinginvoice = Namespace('billing_invoice',description='api to send email')