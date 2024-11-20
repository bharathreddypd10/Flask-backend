from app.app_main import db
from flask_restx import Resource
from flask import request
from app.app_main.models import Services,Users
import uuid

from app.app_main.dto.services import ServicesDto

addnewservice_blueprint=ServicesDto.addnewservice

@addnewservice_blueprint.route('',methods=['POST'])
class AddService(Resource):
    def post(self):
        """Add a new service"""
        data = request.get_json()

        # Validate incoming data
        if not data or 'service_type' not in data or 'price' not in data:
            return {'message': 'Invalid input'}, 400

        # Create a new service instance
        new_service = Services(
            service_id=str(uuid.uuid4()),  # Generate a unique ID
            service_type=data.get('service_type'),
            price=data.get('price')
        )

        # Add the new service to the database
        db.session.add(new_service)
        db.session.commit()

        return {'message': 'Service added successfully'}, 201
    
deleteservice_blueprint=ServicesDto.deleteapi
@deleteservice_blueprint.route('/<string:service_id>', methods=['DELETE'])
class DeleteService(Resource):
    def delete(self, service_id):
        """Delete a service by ID"""
        service = Services.query.get(service_id)

        if not service:
            return {'message': 'Service not found'}, 404

        db.session.delete(service)
        db.session.commit()

        return {'message': 'Service deleted successfully'}, 204
    
getservicesapi_blueprint=ServicesDto.getservicesapi
@getservicesapi_blueprint.route('', methods=['GET'])
class GetServices(Resource):
    def get(self):
        """Get all services"""
        services = Services.query.all()
        return [{'id': str(service.service_id), 'service_type': service.service_type, 'price': service.price} for service in services], 200
    


updateservicesapi_blueprint=ServicesDto.updateservicesapi
@updateservicesapi_blueprint.route('/<string:service_id>', methods=['PUT'])
class UpdateService(Resource):
    def put(self, service_id):
        """Update a service by ID"""
        data = request.json
        service = Services.query.get(service_id)

        if not service:
            return {'message': 'Service not found'}, 404

        # Update the service fields
        if 'service_type' in data:
            service.service_type = data['service_type']
        if 'price' in data:
            service.price = data['price']

        db.session.commit()

        return {'message': 'Service updated successfully'}, 200