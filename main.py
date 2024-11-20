from app.app_main import mydb,socketio
from app.app_main import db
from flask_cors import CORS
from app import blueprint

backend= mydb()
CORS(backend)
backend.register_blueprint(blueprint)


if __name__=="__main__":
    socketio.run(backend, debug=True, host="127.0.0.1", port=5000)
