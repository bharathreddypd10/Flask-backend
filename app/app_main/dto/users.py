from flask_restx import Namespace

class UsersDto:
    signupapi = Namespace('usersignup',description='api for user signup')
    loginapi = Namespace('userlogin',description='api for user login')
    updatedetailsapi = Namespace('updateuser',description='api to update user details')
    deleteapi = Namespace('deleteuser',description='api to delete user account')
    getdetailsapi = Namespace('userdetails',description='api to show details of user')
    passwordcheckapi = Namespace('verifypassword',desciption='api to verify current password')
   