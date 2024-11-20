from app.app_main import db
from flask_restx import Resource
from flask import request
from app.app_main.models import ServiceBookings,Users,Drivers
import uuid

from app.app_main.dto.servicebookings import ServiceBookingsDto

addnewrequest_blueprint=ServiceBookingsDto.addnewrequest

@addnewrequest_blueprint.route('',methods=['POST'])
class addnewrequest(Resource):
    def post(self):
        data = request.get_json()
        email=data.get('email')
        user=Users.query.filter_by(email=email).first()
        
        new_request= ServiceBookings(
            user_id=user.user_id,
            vehicle_type=data.get('vehicleType'),
            vehicle_number=data.get('vehicleNumber'),
            service_type=data.get('serviceType'),   
            preferred_date=data.get('serviceDate'),
            preferred_time=data.get('serviceTime'),
            pickup_location=data.get('location'),
            status='pending'
        )
        try:
            db.session.add(new_request)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'request created successfully'}, 201
    
deleterequest_blueprint=ServiceBookingsDto.deleteapi

@deleterequest_blueprint.route('',methods=['DELETE'])
class deleterequest(Resource):
    def delete(self):
        data =request.get_json()
        booking_id = data.get('booking_id')

        if not booking_id:
            return {'message': 'booking_id is required to delete request'}, 400

        request = ServiceBookings.query.filter_by(booking_id=booking_id).first()

        if not request:
            return {'message': 'Request not found'}, 404

        try:
            db.session.delete(request)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'Request deleted successfully'}, 200
    
getrequests_blueprint=ServiceBookingsDto.getrequestsapi

@getrequests_blueprint.route('', methods=['GET'])
@getrequests_blueprint.route('/<string:booking_id>', methods=['GET'])
@getrequests_blueprint.route('/email/<string:email>', methods=['GET'])
@getrequests_blueprint.route('/email/<string:email>/status/<string:status>', methods=['GET'])
@getrequests_blueprint.route('/status/<string:status>', methods=['GET'])
class getrequests(Resource):
    def get(self,booking_id=None,email=None,status=None):

        driver_id = request.args.get('driver_id', None)
        base_query = db.session.query(ServiceBookings, Users).join(Users, ServiceBookings.user_id == Users.user_id)
        # Initialize the response dictionary with empty lists
        response = {
            'requests': [],
            'pending_requests': [],
            'accepted_requests': []
        }
        if booking_id:
            requests = base_query.filter(ServiceBookings.booking_id == booking_id).all()
            if not requests:
                return {'message': 'Booking ID not found'}, 404
            response['requests'] = self.serialize_requests(requests)
        elif email:
            # Get requests by email and status (completed or not)
            if status is not None:
                # Case when email and status are both provided
                if status == 'completed':
                    requests = base_query.filter(Users.email == email, ServiceBookings.status == 'completed').all()
                else:
                    requests = base_query.filter(Users.email == email, ServiceBookings.status != 'completed').all()
            else:
                # Case when only email is provided, return all requests for the email
                requests = base_query.filter(Users.email == email).all()
                
            if not requests:
                return {'message': 'No service requests found for the provided email and status'}, 404
            response['requests'] = self.serialize_requests(requests)

         # Case 3: Get requests by status only
        elif status is not None:
            query = base_query.filter(ServiceBookings.status == status)
            if driver_id:
                query = query.filter(ServiceBookings.driver_id == driver_id)
            requests = query.all()
            if not requests:
                return {'message': f'No service requests found with status {status}'}, 404
            response['requests'] = self.serialize_requests(requests)

        else:
            pending_requests = base_query.filter(ServiceBookings.status == 'pending').all()
            accepted_requests = base_query.filter(ServiceBookings.status == 'accepted').all()
            if not pending_requests and not accepted_requests:
                return {'message': 'No pending or accepted service requests found'}, 404
            # Populate pending and accepted requests in the response
            response['pending_requests'] = self.serialize_requests(pending_requests)
            response['accepted_requests'] = self.serialize_requests(accepted_requests)
        return response, 200
    
    # Combine the serialization of pending and accepted requests
    def serialize_requests(self,requests):
        return [{
            'booking_id': str(req.ServiceBookings.booking_id),
            'customerName': f"{req.Users.firstName} {req.Users.lastName}",
            'email': req.Users.email,
            'user_id':str(req.Users.user_id),
            'mobile_number': req.Users.phoneNumber,
            'vehicle_type': req.ServiceBookings.vehicle_type,
            'vehicle_number': req.ServiceBookings.vehicle_number,
            'service_type': req.ServiceBookings.service_type,
            'preferred_date': str(req.ServiceBookings.preferred_date),
            'preferred_time': str(req.ServiceBookings.preferred_time),
            'pickup_location': req.ServiceBookings.pickup_location,
            'status': req.ServiceBookings.status,
            'driver_id':str(req.ServiceBookings.driver_id) if req.ServiceBookings.driver_id is not None else None
        } for req in requests]

updaterequest_blueprint=ServiceBookingsDto.updaterequestsapi

@updaterequest_blueprint.route('/<string:booking_id>',methods=['PUT'])
class updateRequestStatus(Resource):
    def put(self, booking_id):
        # Parse request body to get the new status
        data = request.get_json()
        new_status = data.get('status')
        driver_id = data.get('driver_id')  # This can be None if not provided

        try:
            # Step 1: Check if the booking exists
            booking = ServiceBookings.query.filter_by(booking_id=booking_id).first()
            if not booking:
                return {'message': 'Request not found'}, 404
            
            # Step 2: Prepare update data for ServiceBookings table
            update_data = {}
            if new_status:  # Update status if provided
                update_data['status'] = new_status
            
            if driver_id:  # Update driver_id if provided
                update_data['driver_id'] = driver_id
                # Update the driver's status to 'busy' if a driver is assigned and request is not completed
                if new_status != 'completed':
                    driver = Drivers.query.filter_by(driver_id=driver_id).first()
                    if driver:
                        driver.status = 'busy'  # Update the status of the driver to 'busy'
                    else:
                        return {'message': 'Driver not found'}, 404
            
            # Step 3: Update the ServiceBookings table
            if update_data:  # Only update if there's something to update
                ServiceBookings.query.filter_by(booking_id=booking_id).update(update_data)

            # Step 4: If status is 'completed', set the assigned driver's status to 'free'
            if new_status == 'completed' and booking.driver_id:
                driver = Drivers.query.filter_by(driver_id=booking.driver_id).first()
                if driver:
                    driver.status = 'free'  # Set the driver status to 'free' if request is completed

            # Step 5: Commit the changes to the database
            db.session.commit()

            return {
                'message': 'Request updated successfully',
                'status': new_status,
                'driver_id': driver_id,
                'driver_name':driver.driver_name,
                'user_id':str(booking.user_id),
                'email':Users.query.filter_by(user_id=booking.user_id).first().email,
            }, 200

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return {'message': str(e)}, 500
