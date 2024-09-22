

from flask_restx import Namespace, Resource, fields
from utils.DBConnector import db
from datetime import datetime
import hashlib

# Definerer namespace
api = Namespace('companies', description="Company management operations")

# Model for company data
company_model = api.model('companies', {
    'CEO': fields.String(required=True, description='Company CEO'),
    'about': fields.String(required=True, description='Company about section'),
    'address': fields.String(required=True, description='Company address'),
    'company_logo': fields.String(required=True, description='Company logo URL'),
    'email': fields.String(required=True, description='Company email'),
    'org_number':fields.String(required=True, description='Company org number'),
    'phone_number': fields.String(required=True, description='Company phone number'),
    'employees_count': fields.Integer(required=True, description='Number of employees'),
    'role': fields.String(required=True, description='Company role'),
    'country': fields.String(required=True, description='Company country'),
    'website': fields.String(required=True, description='Company website'),
    'images': fields.List(fields.String, required=True, description='List of image URLs'),
    'uid': fields.String(required=True, description='User ID'),
})

# Sjekk om uid eksisterer i 'users' collection
def validate_uid(uid):
    user_ref = db.collection('users').document(uid)
    return user_ref.get().exists

# Endepunkt for å registrere en ny bedrift
@api.route('/create')
class CreateCompany(Resource):
    @api.expect(company_model)
    def post(self):
        data = api.payload
        uid = data['uid']
        
        # Valider at uid eksisterer i 'users' collection
        if not validate_uid(uid):
            return {'message': 'User ID does not exist'}, 400
        
        # Generer document ID basert på org_number og company_name
        cid = hashlib.sha256(f"{data['org_number']}-{data['company_name']}".encode('utf-8')).hexdigest()
        
        # Sjekk om selskapet allerede eksisterer
        company_ref = db.collection('companies').document(cid)
        if company_ref.get().exists:
            return {'message': 'Company with this organization number and name already exists'}, 400
        
        # Lagre selskapet i Firebase
        company_data = {
            'CEO': data['CEO'],
            'about': data['about'],
            'address': data['address'],
            'company_logo': data['company_logo'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'employees_count': data['employees_count'],
            'role': data['role'],
            'country': data['country'],
            'website': data['website'],
            'images': data['images'],
            'uid': data['uid'],
            'cid': cid  # Legger til cid i dokumentet
        }
        
        company_ref.set(company_data)
        
        return {'message': 'Company registered successfully', 'cid': cid}, 201

# Endepunkt for å hente alle selskaper
@api.route('/getAll')
class GetAllCompanies(Resource):
    def get(self):
        companies = []
        company_ref = db.collection('companies').get()
        
        for company in company_ref:
            companies.append(company.to_dict())
        
        return {'companies': companies}, 200

# Endepunkt for å hente et selskap basert på uid
@api.route('/getById/<string:uid>')
class GetCompanyByUID(Resource):
    def get(self, uid):
        # Valider at uid eksisterer i 'users' collection
        if not validate_uid(uid):
            return {'message': 'User ID does not exist'}, 400
        
        # Søk etter selskaper knyttet til uid
        company_ref = db.collection('companies').where('uid', '==', uid).get()
        if not company_ref:
            return {'message': 'No companies found for this user'}, 404
        
        companies = [company.to_dict() for company in company_ref]
        return {'companies': companies}, 200

# Endepunkt for å oppdatere en eksisterende bedrift basert på uid
@api.route('/edit/<string:uid>')
class UpdateCompany(Resource):
    @api.expect(company_model)
    def put(self, uid):
        # Valider at uid eksisterer i 'users' collection
        if not validate_uid(uid):
            return {'message': 'User ID does not exist'}, 400
        
        data = api.payload
        
        # Søk etter selskapet basert på uid
        company_ref = db.collection('companies').where('uid', '==', uid).get()
        if not company_ref:
            return {'message': 'Company not found'}, 404
        
        # Hent det første selskapet knyttet til uid
        company_doc = company_ref[0]
        cid = company_doc.id
        
        # Feltene som kan oppdateres
        update_data = {
            'CEO': data['CEO'],
            'about': data['about'],
            'address': data['address'],
            'company_logo': data['company_logo'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'employees_count': data['employees_count'],
            'role': data['role'],
            'country': data['country'],
            'website': data['website'],
            'images': data['images'],
        }
        
        # Oppdater selskapet i Firebase
        db.collection('companies').document(cid).update(update_data)
        
        return {'message': 'Company updated successfully'}, 200

# Endepunkt for å slette en bedrift basert på uid
@api.route('/del/<string:uid>')
class DeleteCompany(Resource):
    def delete(self, uid):
        # Valider at uid eksisterer i 'users' collection
        if not validate_uid(uid):
            return {'message': 'User ID does not exist'}, 400
        
        # Søk etter selskapet basert på uid
        company_ref = db.collection('companies').where('uid', '==', uid).get()
        if not company_ref:
            return {'message': 'Company not found'}, 404
        
        # Hent det første selskapet knyttet til uid
        company_doc = company_ref[0]
        cid = company_doc.id
        
        # Slett selskapet fra Firebase
        db.collection('companies').document(cid).delete()
        
        return {'message': 'Company deleted successfully'}, 200
