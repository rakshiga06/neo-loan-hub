from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PersonalDetails, FinancialDetails, EmploymentDetails, UserDocuments
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import logging

users_bp = Blueprint('users', __name__)

# Configure file upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------ USER PROFILE ------------------

@users_bp.route('/profile', methods=['GET','PUT'])
@jwt_required()
def get_user_profile():
    try:
        user_id = int(get_jwt_identity())
        user = PersonalDetails.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        profile_data = user.to_dict()
        if user.financial_details:
            profile_data['financial_details'] = user.financial_details.to_dict()
        if user.employment_details:
            profile_data['employment_details'] = user.employment_details.to_dict()
        if user.user_documents:
            profile_data['user_documents'] = user.user_documents.to_dict()

        return jsonify({'profile': profile_data}), 200

    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    try:
        user_id = int(get_jwt_identity())
        user = PersonalDetails.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        print("Received data:", data)

        # Update all required fields safely
        user.full_name = data.get('full_name', user.full_name)
        user.contact_number = data.get('contact_number', user.contact_number)
        user.permanent_address = data.get('permanent_address', user.permanent_address)
        user.gender = data.get('gender', user.gender)
        user.marital_status = data.get('marital_status', user.marital_status)
        user.nationality = data.get('nationality', user.nationality)

        dob_str = data.get('date_of_birth')
        if dob_str:
            try:
                # Accept both date string or ISO format
                if 'T' in dob_str:
                    user.date_of_birth = datetime.fromisoformat(dob_str).date()
                else:
                    user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format for date_of_birth. Use YYYY-MM-DD'}), 400

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ------------------ FINANCIAL DETAILS ------------------

@users_bp.route('/financial-details', methods=['GET','PUT'])
@jwt_required()
def get_financial_details():
    try:
        user_id = int(get_jwt_identity())
        details = FinancialDetails.query.filter_by(user_id=user_id).first()
        if not details:
            return jsonify({'error': 'Financial details not found'}), 404
        return jsonify({'financial_details': details.to_dict()}), 200
    except Exception as e:
        logger.error(f"Get financial details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/financial-details', methods=['POST'])
@jwt_required()
def create_financial_details():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        existing = FinancialDetails.query.filter_by(user_id=user_id).first()
        if existing:
            return jsonify({'error': 'Financial details already exist. Use PUT to update.'}), 400

        details = FinancialDetails(
            user_id=user_id,
            existing_loans=data.get('existing_loans', 0),
            monthly_emi=data.get('monthly_emi', 0),
            assets_owned=data.get('assets_owned'),
            bank_account_details=data.get('bank_account_details', '')
        )
        db.session.add(details)
        db.session.commit()
        return jsonify({'message': 'Financial details created', 'financial_details': details.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create financial details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/financial-details', methods=['PUT'])
@jwt_required()
def update_financial_details():
    try:
        user_id = int(get_jwt_identity())
        details = FinancialDetails.query.filter_by(user_id=user_id).first()
        if not details:
            return jsonify({'error': 'Financial details not found'}), 404

        data = request.get_json()
        details.existing_loans = data.get('existing_loans', details.existing_loans)
        details.monthly_emi = data.get('monthly_emi', details.monthly_emi)
        details.assets_owned = data.get('assets_owned', details.assets_owned)
        details.bank_account_details = data.get('bank_account_details', details.bank_account_details)

        db.session.commit()
        return jsonify({'message': 'Financial details updated', 'financial_details': details.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update financial details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ------------------ EMPLOYMENT DETAILS ------------------

@users_bp.route('/employment-details', methods=['GET','PUT'])
@jwt_required()
def get_employment_details():
    try:
        user_id = int(get_jwt_identity())
        details = EmploymentDetails.query.filter_by(user_id=user_id).first()
        if not details:
            return jsonify({'error': 'Employment details not found'}), 404
        return jsonify({'employment_details': details.to_dict()}), 200
    except Exception as e:
        logger.error(f"Get employment details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/employment-details', methods=['POST'])
@jwt_required()
def create_employment_details():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        existing = EmploymentDetails.query.filter_by(user_id=user_id).first()
        if existing:
            return jsonify({'error': 'Employment details already exist. Use PUT to update.'}), 400

        details = EmploymentDetails(
            user_id=user_id,
            employment_status=data.get('employment_status'),
            employer_name_address=data.get('employer_name_address'),
            job_title=data.get('job_title'),
            monthly_income=data.get('monthly_income', 0),
            other_income=data.get('other_income', 0),
            income_proof_path=data.get('income_proof_path')
        )
        db.session.add(details)
        db.session.commit()
        return jsonify({'message': 'Employment details created', 'employment_details': details.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create employment details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/employment-details', methods=['PUT'])
@jwt_required()
def update_employment_details():
    try:
        user_id = int(get_jwt_identity())
        details = EmploymentDetails.query.filter_by(user_id=user_id).first()
        if not details:
            return jsonify({'error': 'Employment details not found'}), 404

        data = request.get_json()
        details.employment_status = data.get('employment_status', details.employment_status)
        details.employer_name_address = data.get('employer_name_address', details.employer_name_address)
        details.job_title = data.get('job_title', details.job_title)
        details.monthly_income = data.get('monthly_income', details.monthly_income)
        details.other_income = data.get('other_income', details.other_income)
        details.income_proof_path = data.get('income_proof_path', details.income_proof_path)

        db.session.commit()
        return jsonify({'message': 'Employment details updated', 'employment_details': details.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update employment details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ------------------ USER DOCUMENTS ------------------

@users_bp.route('/documents', methods=['GET','PUT'])
@jwt_required()
def get_user_documents():
    try:
        user_id = int(get_jwt_identity())
        documents = UserDocuments.query.filter_by(user_id=user_id).first()
        if not documents:
            return jsonify({'message': 'No documents found'}), 200
        return jsonify({'documents': documents.to_dict()}), 200
    except Exception as e:
        logger.error(f"Get documents error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@users_bp.route('/upload-document', methods=['POST'])
@jwt_required()
def upload_document():
    try:
        user_id = int(get_jwt_identity())
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        document_type = request.form.get('document_type')

        if not document_type:
            return jsonify({'error': 'Document type is required'}), 400
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        user_upload_dir = os.path.join(UPLOAD_FOLDER, f'user_{user_id}')
        os.makedirs(user_upload_dir, exist_ok=True)

        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{document_type}_{timestamp}_{filename}"
        file_path = os.path.join(user_upload_dir, filename)

        file.save(file_path)

        documents = UserDocuments.query.filter_by(user_id=user_id).first()
        if not documents:
            documents = UserDocuments(user_id=user_id)
            db.session.add(documents)

        setattr(documents, f"{document_type}_path", file_path)
        db.session.commit()
        return jsonify({'message': 'Document uploaded', 'documents': documents.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Upload document error: {str(e)}")
        return jsonify({'error': str(e)}), 500
