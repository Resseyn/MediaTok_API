from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, supports_credentials=True)
#jwt_manager = JWTManager(app)
swagger = Swagger(app)  # docs hosted on localhost:5000/apidocs
