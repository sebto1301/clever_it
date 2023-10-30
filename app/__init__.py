from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

JWT_KEY = "ThisIsTheCoolestTaskTagUserAPI"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['JWT_SECRET_KEY'] = JWT_KEY

jwt = JWTManager(app)
db = SQLAlchemy(app)
