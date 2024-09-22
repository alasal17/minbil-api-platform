

from flask_restx import Namespace, Resource, fields
from utils.DBConnector import db
from datetime import datetime
import hashlib

# Definerer namespace
api = Namespace('service', description="Service management operations")

# Service model
service_model = api.model(
    'Service', 
    {
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "estimated_time": fields.Integer(required=True),
        "image_url": fields.String(required=True),
        "price": fields.Float(required=True),
        "tags": fields.List(fields.String()),
        "created_at": fields.String(),  # Blir auto generert
        "updated_at": fields.String(),  # Blir auto generert
        "status": fields.Boolean(),
        "cid": fields.String(required=True)  # Company ID
    }
)

# Funksjon for å generere document id basert på 'title' og 'cid'
def generate_service_id(title, cid):
    service_input = f"{title}-{cid}"
    service_hash = hashlib.sha256(service_input.encode('utf-8')).hexdigest()
    return service_hash

# Sjekk om cid eksisterer i 'users' collection
def validate_cid(cid):
    user_ref = db.collection('company').document(cid)
    return user_ref.get().exists

# Endepunkt for å opprette en ny tjeneste
@api.route('/create/<string:cid>')
class CreateService(Resource):
    @api.expect(service_model)
    def post(self, cid):
        data = api.payload
        title = data['title']
        
        # Valider at uid eksisterer i 'users' collection
        if not validate_cid(cid):
            return {'message': 'User ID does not exist'}, 400
        
        # Generer Service ID (sid)
        sid = generate_service_id(title, cid)
        
        # Sjekk om tjeneste allerede eksisterer basert på title og cid
        service_ref = db.collection('service').document(sid)
        if service_ref.get().exists:
            return {'message': 'Service with this title for the company already exists'}, 400
        
        # Generer tidsstempler
        created_at = datetime.utcnow().isoformat()
        
        # Lagre tjenesten i Firebase
        service_data = {
            'title': title,
            'description': data['description'],
            'estimated_time': data['estimated_time'],
            'image_url': data['image_url'],
            'price': data['price'],
            'tags': data['tags'],
            'createdAt': created_at,
            'updated_at': None,  # Null inntil den blir oppdatert
            'status': data.get('status', True),  # Default til True hvis ikke spesifisert
            'cid': cid,  # Legger til cid (Company ID)
            'sid': sid,
        }
        
        service_ref.set(service_data)
        
        return {'message': 'Service created successfully', 'sid': sid}, 201

# Endepunkt for å hente tjenester basert på cid (Company ID)
@api.route('/getById/<string:cid>')
class GetServiceByCID(Resource):
    def get(self, cid):
        services = []
        service_ref = db.collection('service').where('cid', '==', cid).get()
        
        if not service_ref:
            return {'message': 'No services found for this company'}, 404
        
        for service in service_ref:
            services.append(service.to_dict())
        
        return {'services': services}, 200

# Endepunkt for å hente alle tjenester
@api.route('/getAll', methods=['GET'])
class GetAllServices(Resource):
    def get(self):
        services = []
        service_ref = db.collection('service').get()
        
        for service in service_ref:
            services.append(service.to_dict())
        
        return {'services': services}, 200

# Endepunkt for å oppdatere en eksisterende tjeneste
@api.route('/edit/<string:sid>')
class UpdateService(Resource):
    @api.expect(service_model)
    def put(self, sid):
        data = api.payload
        
        # Hent eksisterende tjeneste fra Firebase
        service_ref = db.collection('service').document(sid)
        service = service_ref.get()
        
        if not service.exists:
            return {'message': 'Service not found'}, 404
        
        # Oppdaterbare felter
        update_data = {
            'description': data['description'],
            'estimated_time': data['estimated_time'],
            'image_url': data['image_url'],
            'price': data['price'],
            'tags': data['tags'],
            'status': data.get('status', True),
            'updated_at': datetime.utcnow().isoformat()  # Auto generert når endret
        }
        
        # Oppdater tjenesten i Firebase
        service_ref.update(update_data)
        
        return {'message': 'Service updated successfully'}, 200

# Endepunkt for å slette en tjeneste basert på sid
@api.route('/delete/<string:sid>')
class DeleteService(Resource):
    def delete(self, sid):
        # Hent eksisterende tjeneste fra Firebase
        service_ref = db.collection('service').document(sid)
        service = service_ref.get()
        
        if not service.exists:
            return {'message': 'Service not found'}, 404
        
        # Slett tjenesten fra Firebase
        service_ref.delete()
        
        return {'message': 'Service deleted successfully'}, 200
