from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # docs hosted on localhost:5000/apidocs
