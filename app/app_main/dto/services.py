from flask_restx import Namespace

class ServicesDto:
    addnewservice = Namespace('addservice',description='api to add new service')
    deleteapi = Namespace('deleteservice',description='api to delete service ')
    getservicesapi = Namespace('getservice',description='api to show services')
    updateservicesapi = Namespace('updateservice',description='api to update service')