from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize JWTManager
jwt = JWTManager(app)

from app.auth.routes import auth_bp
from app.api.routes import api_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

from app import models  # Import your models here
