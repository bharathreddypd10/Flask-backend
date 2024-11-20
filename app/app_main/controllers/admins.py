from flask_restx import Resource
from flask import request
from app.app_main import db
from app.app_main.dto.admin import AdminsDto
from app.app_main.models import Admins

updateadmin_blueprint=AdminsDto.updatedetailsapi

@updateadmin_blueprint.route('',methods=['PUT'])
class adminupdate(Resource):
    def put(self):
        data=request.get_json()
        email = data.get('email')

        admin = Admins.query.filter_by(email=email).first()

        if not admin:
            return {'message': 'User not found'}, 404    
        
        admin.adminName=data.get('adminName',admin.adminName)
        admin.phoneNumber=data.get('phoneNumber',admin.phoneNumber)
        admin.email=data.get('email',admin.email)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'admin updated successfully',
                'admin':{
                    'email': admin.email,
                    'adminName':admin.adminName,
                    'phoneNumber':admin.phoneNumber    
                }}, 200
