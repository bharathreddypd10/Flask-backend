from flask_restx import Resource
from flask import request
from app.app_main import db
from app.app_main.models import Drivers,ServiceBookings
import uuid
from app.app_main.dto.drivers import DriversDto

adddriver_blueprint=DriversDto.adddriver

@adddriver_blueprint.route('',methods=['POST'])
class adddriver(Resource):
    def post(self):
        data = request.get_json()
        driver = Drivers.query.filter_by(driver_email=data['driver_email']).first()
        if driver:
            return {'message': 'driver already exists'},400
        
        new_driver= Drivers(
            # driver_id = str(uuid.uuid4()),
            driver_name=data.get('driver_name'),
            driver_age=data.get('driver_age'),
            driver_email=data.get('driver_email'),   
            driver_mobile=data.get('driver_mobile')
        )
        new_driver.set_password(data.get('driver_password'))

        try:
            db.session.add(new_driver)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'Driver Added successfully'}, 201
    


updatedriver_blueprint=DriversDto.updatedriver
@updatedriver_blueprint.route('/<string:driver_id>', methods=['PUT'])
class UpdateDriver(Resource):
    def put(self, driver_id):
        data = request.get_json()
        driver = Drivers.query.filter_by(driver_id=driver_id).first()        
        if not driver:
            return {'message': 'Driver not found'}, 404

        # Update driver details if provided in the request
        driver.driver_name = data.get('driver_name', driver.driver_name)
        driver.driver_age = data.get('driver_age', driver.driver_age)
        driver.driver_email = data.get('driver_email', driver.driver_email)
        driver.driver_mobile = data.get('driver_mobile', driver.driver_mobile)
        driver.status = data.get('status', driver.status)

        try:
            db.session.commit()
            return {'message': 'Driver updated successfully',
                    'driver': {
                    'driver_id': str(driver.driver_id),
                    'driver_name': driver.driver_name,
                    'driver_age': driver.driver_age,
                    'driver_email': driver.driver_email,
                    'driver_mobile': driver.driver_mobile,
                    'status': driver.status
                }}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
        
deletedriver_blueprint=DriversDto.deletedriver
@deletedriver_blueprint.route('/<string:driver_id>', methods=['DELETE'])
class DeleteDriver(Resource):
    def delete(self, driver_id):
        driver = Drivers.query.filter_by(driver_id=driver_id).first()
        
        if not driver:
            return {'message': 'Driver not found'}, 404
        
        try:
            db.session.delete(driver)
            db.session.commit()
            return {'message': 'Driver deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
        
getdriver_blueprint=DriversDto.getdriverdetails
@getdriver_blueprint.route('', methods=['GET'])
@getdriver_blueprint.route('/<string:status>', methods=['GET'])
@getdriver_blueprint.route('/<string:booking_id>', methods=['GET'])
class GetDrivers(Resource):
    def get(self,status=None,booking_id=None):
        booking_id = request.args.get('booking_id')  # Get booking_id from query parameters
        status = request.args.get('Status')
        try:
            query = db.session.query(Drivers)
            # Case 1: If booking_id is provided, join ServiceBookings and filter by booking_id
            if booking_id:
                driver = (
                    query.join(ServiceBookings, Drivers.driver_id == ServiceBookings.driver_id)
                    .filter(ServiceBookings.booking_id == booking_id)
                    .first()
                )
                if driver:
                    return {'driver': [driver.to_dict()]}, 200
                else:
                    return {'message': 'Driver not found for the provided booking ID'}, 404

            # Case 2: If status is provided (and booking_id is not), filter by status in Drivers table
            elif status:
                drivers = query.filter_by(status=status).all()
                if drivers:
                    drivers_data = [driver.to_dict() for driver in drivers]  # Convert to dict for all drivers
                    return {'drivers': drivers_data}, 200
                else:
                    return {'message':' No drivers found'},200
            # Case 3: If neither booking_id nor status is provided, get all drivers
            else:
                drivers = query.all()
                drivers_data = [driver.to_dict() for driver in drivers]
                return {'drivers': drivers_data}, 200

        except Exception as e:
            return {'message': str(e)}, 500






