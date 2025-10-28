from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, FinancialInfo, KYCDocument
from datetime import datetime
import os
from werkzeug.utils import secure_filename

users_bp = Blueprint('users', __name__)

# Configure file upload
UPLOAD_FOLDER = 'uploads/kyc'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile_data = user.to_dict()
        
        # Add financial info if exists
        if user.financial_info:
            profile_data['financial_info'] = user.financial_info.to_dict()
        
        # Add KYC documents
        kyc_docs = KYCDocument.query.filter_by(user_id=user_id).all()
        profile_data['kyc_documents'] = [doc.to_dict() for doc in kyc_docs]
        
        return jsonify({'profile': profile_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'address' in data:
            user.address = data['address']
        if 'date_of_birth' in data and data['date_of_birth']:
            user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/financial-info', methods=['GET'])
@jwt_required()
def get_financial_info():
    try:
        user_id = get_jwt_identity()
        financial_info = FinancialInfo.query.filter_by(user_id=user_id).first()
        
        if not financial_info:
            return jsonify({'error': 'Financial information not found'}), 404
        
        return jsonify({'financial_info': financial_info.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/financial-info', methods=['POST'])
@jwt_required()
def create_financial_info():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if financial info already exists
        existing_info = FinancialInfo.query.filter_by(user_id=user_id).first()
        if existing_info:
            return jsonify({'error': 'Financial information already exists. Use PUT to update.'}), 400
        
        # Create new financial info
        financial_info = FinancialInfo(
            user_id=user_id,
            employment_status=data.get('employment_status'),
            annual_income=data.get('annual_income'),
            credit_score=data.get('credit_score'),
            existing_loans=data.get('existing_loans', 0),
            debt_to_income_ratio=data.get('debt_to_income_ratio')
        )
        
        db.session.add(financial_info)
        db.session.commit()
        
        return jsonify({
            'message': 'Financial information created successfully',
            'financial_info': financial_info.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/financial-info', methods=['PUT'])
@jwt_required()
def update_financial_info():
    try:
        user_id = get_jwt_identity()
        financial_info = FinancialInfo.query.filter_by(user_id=user_id).first()
        
        if not financial_info:
            return jsonify({'error': 'Financial information not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'employment_status' in data:
            financial_info.employment_status = data['employment_status']
        if 'annual_income' in data:
            financial_info.annual_income = data['annual_income']
        if 'credit_score' in data:
            financial_info.credit_score = data['credit_score']
        if 'existing_loans' in data:
            financial_info.existing_loans = data['existing_loans']
        if 'debt_to_income_ratio' in data:
            financial_info.debt_to_income_ratio = data['debt_to_income_ratio']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Financial information updated successfully',
            'financial_info': financial_info.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/kyc-documents', methods=['GET'])
@jwt_required()
def get_kyc_documents():
    try:
        user_id = get_jwt_identity()
        kyc_docs = KYCDocument.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'kyc_documents': [doc.to_dict() for doc in kyc_docs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/kyc-documents', methods=['POST'])
@jwt_required()
def upload_kyc_document():
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        document_type = request.form.get('document_type')
        document_number = request.form.get('document_number')
        
        if not document_type or not document_number:
            return jsonify({'error': 'Document type and document number are required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Only PDF, PNG, JPG, JPEG are allowed'}), 400
        
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(file_path)
        
        # Create KYC document record
        kyc_doc = KYCDocument(
            user_id=user_id,
            document_type=document_type,
            document_number=document_number,
            document_file_path=file_path,
            status='Pending'
        )
        
        db.session.add(kyc_doc)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'kyc_document': kyc_doc.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/kyc-documents/<int:kyc_id>', methods=['DELETE'])
@jwt_required()
def delete_kyc_document(kyc_id):
    try:
        user_id = get_jwt_identity()
        kyc_doc = KYCDocument.query.filter_by(kyc_id=kyc_id, user_id=user_id).first()
        
        if not kyc_doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete file from filesystem
        if kyc_doc.document_file_path and os.path.exists(kyc_doc.document_file_path):
            os.remove(kyc_doc.document_file_path)
        
        # Delete from database
        db.session.delete(kyc_doc)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
