from datetime import datetime,timedelta
from flask_restx import Resource
from flask import request,current_app,jsonify,url_for,render_template,send_from_directory
from app.app_main import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.app_main.models import Users,Admins,Drivers
import uuid
from marshmallow import ValidationError
from app.app_main.schemas.users import UserRegistrationSchema,UserLoginSchema,UserUpdateSchema,PasswordChangeSchema 

from app.app_main.dto.users import UsersDto

signup_blueprint=UsersDto.signupapi

#usersignup
@signup_blueprint.route('',methods=['POST'])
class signup(Resource):
    def post(self):
        schema = UserRegistrationSchema()
        data = request.get_json()

        # Validate the input data
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        user = Users.query.filter_by(email=validated_data['email']).first()

        if user:
            return {'message': 'user already exists'},400
        
        new_user= Users(
            user_id = str(uuid.uuid4()),
            **validated_data
        )
        new_user.set_password(validated_data.get('password'))

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'User created successfully'}, 201


login_blueprint=UsersDto.loginapi

#userlogin
@login_blueprint.route('',methods=['POST'])
class userlogin(Resource):
    def post(self):
        schema = UserLoginSchema()
        data = request.get_json()
        # Validate input data
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            role='user'
            access_token = create_access_token(
                identity=user.user_id,
                expires_delta=timedelta(minutes=15),
                additional_claims={
                    'email':user.email,
                    'firstName':user.firstName,
                    'lastName':user.lastName,
                    'phoneNumber':user.phoneNumber,
                    'address':user.address
                    })
            return {'message': 'Login successful','token':access_token,'role':role}, 200
        
        admin = Admins.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            role = 'admin'
            access_token = create_access_token(
                identity=admin.admin_id, 
                expires_delta=timedelta(minutes=15),
                additional_claims={
                    'email': admin.email,
                    'adminName': admin.adminName,
                    'phoneNumber': admin.phoneNumber,
                }
            )
            return {'message': 'Login successful', 'token': access_token,'role':role}, 200
        
        # Check for driver login
        driver = Drivers.query.filter_by(driver_email=email).first()
        if driver and driver.check_password(password):
            role = 'driver'
            access_token = create_access_token(
                identity=driver.driver_id,
                expires_delta=timedelta(minutes=15),
                additional_claims={
                    'driver_name': driver.driver_name,
                    'driver_email': driver.driver_email,
                    'driver_mobile': driver.driver_mobile,
                    'driver_age': driver.driver_age
                }
            )
            return {'message': 'Login successful', 'token': access_token, 'role': role}, 200
        else:
            return {'message': 'Invalid email or password'}, 401
        

update_blueprint=UsersDto.updatedetailsapi

#updateuser
@update_blueprint.route('',methods=['PUT'])
class userupdate(Resource):
    def put(self):
        schema = UserUpdateSchema()
        data=request.get_json()

        # Validate input data
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        email = validated_data.get('email')

        user = Users.query.filter_by(email=email).first()

        if not user:
            return {'message': 'User not found'}, 404    
        
        user.firstName=validated_data.get('firstName',user.firstName)
        user.lastName=validated_data.get('lastName',user.lastName)
        user.phoneNumber=validated_data.get('phoneNumber',user.phoneNumber)
        user.address=validated_data.get('address',user.address)

        if "password" in data:
            user.set_password(validated_data['password'])

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'User updated successfully',
                'user':{
                    'email':email,
                    'firstName':user.firstName,
                    'lastName':user.lastName,
                    'phoneNumber':user.phoneNumber,
                    'address':user.address
                }}, 200


delete_blueprint=UsersDto.deleteapi

#deleteuser
@delete_blueprint.route('',methods=['DELETE'])
class delete(Resource):
    def delete(self):
        data =request.get_json()
        email = data.get('email')

        if not email:
            return {'message': 'Email is required to delete user'}, 400

        user = Users.query.filter_by(email=email).first()

        if not user:
            return {'message': 'User not found'}, 404

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'User deleted successfully'}, 200

details_blueprint=UsersDto.getdetailsapi

#getdetails
@details_blueprint.route('',methods=['GET'])
class userdetais(Resource):
    def get(self):
        email = request.args.get('email')

        if email:
            user = Users.query.filter_by(email=email).first()

            if not user:
                return {'message': 'User not found'}, 404
        
            user_data = {
                'user_id': str(user.user_id),
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'phoneNumber': user.phoneNumber,
                'address': user.address
            }
            return {'user': user_data}, 200
        else:
            # Fetch all users
            users = Users.query.all()

            if not users:
                return {'message': 'No users found'}, 404

            all_users_data = []
            for user in users:
                user_data = {
                    'user_id': str(user.user_id),
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'phoneNumber': user.phoneNumber,
                    'address': user.address
                }
                all_users_data.append(user_data)

            return {'users': all_users_data}, 200
        
verifypassword_blueprint=UsersDto.passwordcheckapi
@verifypassword_blueprint.route('',methods=['POST'])
class validatecurrentpassword(Resource):
    @jwt_required()
    def post(self):
        schema = PasswordChangeSchema()
        # Get the current password from the request body
        data = request.get_json()
        # Validate input data
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        current_password = validated_data.get('currentPassword')

        # Get the user id from the JWT token
        user_id = get_jwt_identity()

        # Try to find the user in the Users table first
        user = Users.query.get(user_id)

        if user and user.check_password(current_password):
            user.set_password(validated_data['newPassword'])
            try:
                db.session.commit()
                return {"message": "Current password is valid and new password is set."}, 200
            except Exception as e:
                db.session.rollback()
                return {'message': str(e)}, 500
            

        # If not found in Users, check the Admins table
        admin = Admins.query.get(user_id)

        if admin and admin.check_password(current_password):
            admin.set_password(validated_data['newPassword'])
            try:
                db.session.commit()  # Save the new password
                return {"message": "Current password is valid and new password is set."}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 500

        # If not found in Admins, check the Drivers table
        driver = Drivers.query.get(user_id)

        if driver and driver.check_password(current_password):
            driver.set_password(validated_data['newPassword'])
            try:
                db.session.commit()  # Save the new password
                return {"message": "Current password is valid and new password is set."}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 500

        # If the password does not match for any role, return an error
        return {"message": "Current password is invalid."}, 401