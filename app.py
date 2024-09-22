from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from apis import api
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env')
cors = CORS()
app = Flask(__name__)
cors.init_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)

port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host='0.0.0.0', port=port)