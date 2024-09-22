# from flask import Flask
# from werkzeug.middleware.proxy_fix import ProxyFix
# from apis.company_endpoint import api as capi 
# from apis.services_api import api as sapi 
# from apis.users_api import api as uapi 
# from flask_restx import Api

# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# load_dotenv(dotenv_path='.env')
# cors = CORS()
# app = Flask(__name__)
# api = Api(app, 
#     title="MinBil API",
#     version="1.0",
#     description="MinBil API for managing vehicles and services",
#     doc="/swagger-ui",
#     swagger_ui_css='https://my-custom-css-url.com/swagger-custom.css', # Custom CSS
#     swagger_ui_config={
#         'displayRequestDuration': True,
#         'docExpansion': 'none',
#         'defaultModelsExpandDepth': -1,
#         'customLogo': 'https://my-logo-url.com/logo.png',  # Custom logo
#         'customSiteTitle': "MinBil API Documentation",
#         'favicon': 'https://my-favicon-url.com/favicon.ico',  # Custom favicon
#     }
# )
# api.add_namespace(capi)
# api.add_namespace(uapi)
# api.add_namespace(sapi)
# cors.init_app(app)
# app.wsgi_app = ProxyFix(app.wsgi_app)
# api.init_app(app)

# port = int(os.environ.get("PORT", 5000))

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from apis.companies_endpoints import api as capi 
from apis.services_endpoints import api as sapi 
from apis.users_endpoints import api as uapi 
from flask_restx import Api

from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env')
cors = CORS()

app = Flask(__name__)

# Initialize the API and directly pass the app here
api = Api(app, 
    title="MinBil API",
    version="1.0",
    description="MinBil API for managing vehicles and services",
    doc="/swagger-ui",
    swagger_ui_css='https://mbb-swagger-custom-api.anez.no/swagger-custom.css',  # Custom CSS
    swagger_ui_config={
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'defaultModelsExpandDepth': -1,
        'customLogo': 'https://my-logo-url.com/logo.png',  # Custom logo
        'customSiteTitle': "MinBil API Documentation",
        'favicon': 'https://my-favicon-url.com/favicon.ico',  # Custom favicon
    }
)

# Register the namespaces
api.add_namespace(capi)
api.add_namespace(uapi)
api.add_namespace(sapi)

cors.init_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

# The api.init_app(app) call is removed since you've already initialized the API with app

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
