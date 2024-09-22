from flask_restx import Api, reqparse
from .companies_endpoints import api as ca
from .users_endpoints import api as ua
from .services_endpoints import api as sa
from flask import jsonify, request

# api = Api(
#     title="MinBil API",
#     version="1.0",
#     description="MinBil API for managing vehicles and services"

#     )



# api.add_namespace(ca)
# api.add_namespace(ua)
# api.add_namespace(sa)
