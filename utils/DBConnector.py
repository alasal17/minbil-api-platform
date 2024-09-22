import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

# Last inn miljøvariabler fra .env-filen
load_dotenv(dotenv_path='.env')

# Hent miljøvariabler
project_id = os.getenv('PROJECT_ID')
private_key_id = os.getenv('PRIVATE_KEY_ID')
private_key = os.getenv('PRIVATE_KEY')
client_email = os.getenv('CLIENT_EMAIL')
client_id = os.getenv('CLIENT_ID')
auth_uri = os.getenv('AUTH_URI')
token_uri = os.getenv('TOKEN_URI')
auth_provider_x509_cert_url = os.getenv('AUTH_PROVIDER_X509_CERT_URL')
client_x509_cert_url = os.getenv('CLIENT_X509_CERT_URL')

# Behandle private_key med stripping og newline-tegn
if private_key is not None:
    private_key = private_key.strip().replace('\\n', '\n')
else:
    raise ValueError("PRIVATE_KEY is not set in .env file")

# Konfigurasjonsordbok for Firebase
config = {
    "type": "service_account",
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url
}

# Initialiser Firebase-appen
cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred)

# Koble til Firestore
db = firestore.client()
