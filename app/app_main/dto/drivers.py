from flask_restx import Namespace

class DriversDto:
    adddriver = Namespace('adddriver',description='api for adding driver')
    updatedriver = Namespace('updatedriver',description='api to update driver details')
    deletedriver = Namespace('deletedriver',description='api to delete driver account')
    getdriverdetails = Namespace('getdriverdetails',description='api to show details of driver')