from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_mail import Mail
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
socketio = SocketIO(async_mode="eventlet")  # Initialize SocketIO here
# Load environment variables from sendgrid.env
load_dotenv('sendgrid.env')

def mydb():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:password1234@127.0.0.1/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SECRET_KEY']="7a4b1e68ef1e4fb29b3f12a29d3ec4d8e3f71b24509c11d0"

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'  # or your SMTP server (e.g., smtp.gmail.com)
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'apikey'
    app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
    app.config['MAIL_DEFAULT_SENDER'] = 'vehicleservicemanagement70@gmail.com'
    app.config['MAIL_SUPPRESS_SEND'] = False  # Set to True to suppress sending in development

    db.init_app(app)
    migrate.init_app(app,db)
    JWTManager(app)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")  # WebSocket support with CORS allowed
    from app.app_main.models import Users, Admins,ServiceBookings,services,Drivers,Notifications
    from app.app_main.controllers import socket_events

    return app