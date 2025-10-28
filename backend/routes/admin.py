from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loan, LoanProduct, User, FinancialInfo, KYCDocument, AdminBank
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # In a real application, you would check if the user has admin privileges
        # For now, we'll use a simple check - you can implement proper admin authentication
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Simple admin check - in production, you'd have a proper admin role system
        if not user or user.email != 'admin@loanhub.com':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/banks', methods=['GET'])
@jwt_required()
@admin_required
def get_banks():
    try:
        banks = AdminBank.query.all()
        return jsonify({
            'banks': [bank.to_dict() for bank in banks]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/banks', methods=['POST'])
@jwt_required()
@admin_required
def create_bank():
    try:
        data = request.get_json()
        
        required_fields = ['bank_name', 'contact_email', 'contact_phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if bank already exists
        existing_bank = AdminBank.query.filter_by(bank_name=data['bank_name']).first()
        if existing_bank:
            return jsonify({'error': 'Bank with this name already exists'}), 400
        
        bank = AdminBank(
            bank_name=data['bank_name'],
            contact_email=data['contact_email'],
            contact_phone=data['contact_phone'],
            address=data.get('address')
        )
        
        db.session.add(bank)
        db.session.commit()
        
        return jsonify({
            'message': 'Bank created successfully',
            'bank': bank.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loan-products', methods=['GET'])
@jwt_required()
@admin_required
def get_all_loan_products():
    try:
        loan_products = LoanProduct.query.all()
        return jsonify({
            'loan_products': [product.to_dict() for product in loan_products]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loan-products', methods=['POST'])
@jwt_required()
@admin_required
def create_loan_product():
    try:
        data = request.get_json()
        
        required_fields = ['bank_id', 'product_name', 'min_amount', 'max_amount', 'interest_rate']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if bank exists
        bank = AdminBank.query.get(data['bank_id'])
        if not bank:
            return jsonify({'error': 'Bank not found'}), 404
        
        loan_product = LoanProduct(
            bank_id=data['bank_id'],
            product_name=data['product_name'],
            description=data.get('description'),
            min_amount=data['min_amount'],
            max_amount=data['max_amount'],
            interest_rate=data['interest_rate'],
            tenure_range=data.get('tenure_range'),
            eligibility_criteria=data.get('eligibility_criteria')
        )
        
        db.session.add(loan_product)
        db.session.commit()
        
        return jsonify({
            'message': 'Loan product created successfully',
            'loan_product': loan_product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loan-products/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_loan_product(product_id):
    try:
        loan_product = LoanProduct.query.get(product_id)
        if not loan_product:
            return jsonify({'error': 'Loan product not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'product_name' in data:
            loan_product.product_name = data['product_name']
        if 'description' in data:
            loan_product.description = data['description']
        if 'min_amount' in data:
            loan_product.min_amount = data['min_amount']
        if 'max_amount' in data:
            loan_product.max_amount = data['max_amount']
        if 'interest_rate' in data:
            loan_product.interest_rate = data['interest_rate']
        if 'tenure_range' in data:
            loan_product.tenure_range = data['tenure_range']
        if 'eligibility_criteria' in data:
            loan_product.eligibility_criteria = data['eligibility_criteria']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Loan product updated successfully',
            'loan_product': loan_product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loans', methods=['GET'])
@jwt_required()
@admin_required
def get_all_loans():
    try:
        status = request.args.get('status')
        bank_id = request.args.get('bank_id', type=int)
        
        query = Loan.query
        
        if status:
            query = query.filter_by(status=status)
        
        if bank_id:
            query = query.join(LoanProduct).filter(LoanProduct.bank_id == bank_id)
        
        loans = query.order_by(Loan.application_date.desc()).all()
        
        return jsonify({
            'loans': [loan.to_dict() for loan in loans]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loans/<int:loan_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        if loan.status != 'Pending':
            return jsonify({'error': 'Only pending loans can be approved'}), 400
        
        loan.status = 'Approved'
        loan.approval_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Loan approved successfully',
            'loan': loan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/loans/<int:loan_id>/reject', methods=['POST'])
@jwt_required()
@admin_required
def reject_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        if loan.status != 'Pending':
            return jsonify({'error': 'Only pending loans can be rejected'}), 400
        
        data = request.get_json()
        rejection_reason = data.get('rejection_reason', 'No reason provided')
        
        loan.status = 'Rejected'
        loan.approval_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Loan rejected successfully',
            'loan': loan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/kyc-documents', methods=['GET'])
@jwt_required()
@admin_required
def get_all_kyc_documents():
    try:
        status = request.args.get('status')
        
        query = KYCDocument.query
        
        if status:
            query = query.filter_by(status=status)
        
        kyc_docs = query.order_by(KYCDocument.uploaded_at.desc()).all()
        
        return jsonify({
            'kyc_documents': [doc.to_dict() for doc in kyc_docs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/kyc-documents/<int:kyc_id>/verify', methods=['POST'])
@jwt_required()
@admin_required
def verify_kyc_document(kyc_id):
    try:
        kyc_doc = KYCDocument.query.get(kyc_id)
        if not kyc_doc:
            return jsonify({'error': 'KYC document not found'}), 404
        
        data = request.get_json()
        status = data.get('status')  # 'Verified' or 'Rejected'
        
        if status not in ['Verified', 'Rejected']:
            return jsonify({'error': 'Status must be either Verified or Rejected'}), 400
        
        kyc_doc.status = status
        kyc_doc.verified_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'KYC document {status.lower()} successfully',
            'kyc_document': kyc_doc.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
    try:
        # Total users
        total_users = User.query.count()
        
        # Total loans
        total_loans = Loan.query.count()
        
        # Loans by status
        pending_loans = Loan.query.filter_by(status='Pending').count()
        approved_loans = Loan.query.filter_by(status='Approved').count()
        rejected_loans = Loan.query.filter_by(status='Rejected').count()
        active_loans = Loan.query.filter_by(status='Active').count()
        
        # Pending KYC documents
        pending_kyc = KYCDocument.query.filter_by(status='Pending').count()
        
        # Total loan amount
        total_loan_amount = db.session.query(db.func.sum(Loan.loan_amount)).filter_by(status='Active').scalar() or 0
        
        return jsonify({
            'total_users': total_users,
            'total_loans': total_loans,
            'pending_loans': pending_loans,
            'approved_loans': approved_loans,
            'rejected_loans': rejected_loans,
            'active_loans': active_loans,
            'pending_kyc': pending_kyc,
            'total_loan_amount': float(total_loan_amount)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
