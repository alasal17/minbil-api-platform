from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from utils.DBConnector import db  # Antar at DBConnector er konfigurert for Firebase
from datetime import datetime
import hashlib

# Definerer namespace
api = Namespace('users', description="User registration and login operations")

# Request parsers for registration og login
registration_model = api.model('Register', {
    'display_name': fields.String(required=True, description='Display name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
})

# Funksjon for å generere uid
def generate_uid(display_name, email):
    uid_input = f"{display_name}-{email}"
    uid_hash = hashlib.sha256(uid_input.encode('utf-8')).hexdigest()
    return uid_hash

# Sjekker om email er valid
def validate_email(email):
    if '@' not in email:
        return False
    return True

# Registrerings-endepunkt
@api.route('/register')
class Register(Resource):
    @api.expect(registration_model)
    def post(self):
        data = api.payload
        display_name = data['display_name']
        email = data['email']
        password = data['password']
        
        # Valider email
        if not validate_email(email):
            return {'message': 'Invalid email format'}, 400
        
        # Generer UID
        uid = generate_uid(display_name, email)
        
        # Sjekk om bruker allerede eksisterer (document id = uid)
        user_ref = db.collection('users').document(uid)
        if user_ref.get().exists:
            return {'message': 'User already exists'}, 400
        
        # Krypter passordet
        hashed_password = generate_password_hash(password)
        
        # Lagre brukerdata i Firebase
        user_data = {
            'createdAt': datetime.utcnow().isoformat(),
            'display_name': display_name,
            'email': email,
            'password': hashed_password,
            'uid': uid,
        }
        
        user_ref.set(user_data)
        
        return {'message': 'User registered successfully', 'uid': uid}, 201


# Innloggings-endepunkt
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = api.payload
        email = data['email']
        password = data['password']
        
        # Valider email
        if not validate_email(email):
            return {'message': 'Invalid email format'}, 400
        
        # Søk etter bruker ved hjelp av email
        users_ref = db.collection('users').where('email', '==', email).get()
        if not users_ref:
            return {'message': 'User not found'}, 404
        
        # Hent brukerdata
        user_data = users_ref[0].to_dict()
        stored_password = user_data['password']
        
        # Sammenlign passord
        if not check_password_hash(stored_password, password):
            return {'message': 'Invalid password'}, 401
        
        return {'message': 'Login successful', 'uid': user_data['uid']}, 200
