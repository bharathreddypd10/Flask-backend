from flask_restx import Namespace

class ServiceBookingsDto:
    addnewrequest = Namespace('addrequest',description='api to add new service request')
    deleteapi = Namespace('deleterequest',description='api to delete service request')
    getrequestsapi = Namespace('getrequest',description='api to show requests')
    updaterequestsapi = Namespace('updaterequest',description='api to update status of request')