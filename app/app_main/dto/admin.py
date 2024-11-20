from flask_restx import Namespace

class AdminsDto:
    updatedetailsapi = Namespace('updateadmin',description='api to update admin details')
    deleteapi = Namespace('deleteadmin',description='api to delete admin account')
    getdetailsapi = Namespace('admindetails',description='api to show details of admin')