from flask_restx import Namespace

class NotificationsDto:
    getnotifications = Namespace('getnotifications',description='api for getting notifications')
    updatenotification=Namespace('updatenotification',description='api for updating notification')
    deletenotifications = Namespace('deletenotifications',description='api to delete notifications')
   