from flask_restx import Api, reqparse
from .company_endpoint import api as ca
from .users_api import api as ua
from .services_api import api as sa
from flask import jsonify, request

api = Api(
    doc='/docs',
    title="Minbil-plattform-API",
    version="1.0",
    description="API with Flask-RestX",
    default_mediatype = "application/x-www-form-urlencoded"

    )



api.add_namespace(ca)
api.add_namespace(ua)
api.add_namespace(sa)
