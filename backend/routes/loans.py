from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loan, LoanProduct, PersonalDetails, FinancialDetails, EmploymentDetails
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
loans_bp = Blueprint('loans', __name__)


@loans_bp.route('/products', methods=['GET'])
def get_loan_products():
    """Get all loan products with optional filtering"""
    try:
        bank_id = request.args.get('bank_id', type=int)
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        
        query = LoanProduct.query
        
        if bank_id:
            query = query.filter_by(bank_id=bank_id)
        
        if min_amount:
            query = query.filter(LoanProduct.max_amount >= min_amount)
        
        if max_amount:
            query = query.filter(LoanProduct.min_amount <= max_amount)
        
        loan_products = query.all()
        
        return {'loan_products': [product.to_dict() for product in loan_products]}, 200
        
    except Exception as e:
        logger.error(f"Get loan products error: {str(e)}")
        return {'error': str(e)}, 500


@loans_bp.route('/products/<int:product_id>', methods=['GET'])
def get_loan_product(product_id):
    """Get specific loan product details"""
    try:
        loan_product = LoanProduct.query.get(product_id)
        
        if not loan_product:
            return {'error': 'Loan product not found'}, 404
        
        return {'loan_product': loan_product.to_dict()}, 200
        
    except Exception as e:
        logger.error(f"Get loan product error: {str(e)}")
        return {'error': str(e)}, 500


@loans_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_for_loan():
    """Apply for a loan"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['loan_product_id', 'loan_amount', 'tenure_months']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field} is required'}, 400
        
        # Check if loan product exists
        loan_product = LoanProduct.query.get(data['loan_product_id'])
        if not loan_product:
            return {'error': 'Loan product not found'}, 404
        
        # Validate loan amount
        loan_amount = Decimal(str(data['loan_amount']))
        if loan_amount < loan_product.min_amount or loan_amount > loan_product.max_amount:
            return {
                'error': f'Loan amount must be between {loan_product.min_amount} and {loan_product.max_amount}'
            }, 400
        
        # Check if user already has a pending application for this product
        existing_loan = Loan.query.filter_by(
            user_id=user_id,
            loan_product_id=data['loan_product_id'],
            status='Pending'
        ).first()
        
        if existing_loan:
            return {'error': 'You already have a pending application for this loan product'}, 400
        
        # Calculate EMI
        monthly_rate = loan_product.interest_rate / (12 * 100)
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** data['tenure_months']) / \
              ((1 + monthly_rate) ** data['tenure_months'] - 1)
        
        # Create new loan application
        loan = Loan(
            user_id=user_id,
            loan_product_id=data['loan_product_id'],
            loan_amount=loan_amount,
            tenure_months=data['tenure_months'],
            interest_rate=loan_product.interest_rate,
            monthly_emi=emi,
            status='Pending'
        )
        
        db.session.add(loan)
        db.session.commit()
        
        return {
            'message': 'Loan application submitted successfully',
            'loan': loan.to_dict()
        }, 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Apply for loan error: {str(e)}")
        return {'error': str(e)}, 500


@loans_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_user_loans():
    """Get user's loan applications"""
    try:
        user_id = int(get_jwt_identity())
        status = request.args.get('status')
        
        query = Loan.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        loans = query.order_by(Loan.application_date.desc()).all()
        
        return {'loans': [loan.to_dict() for loan in loans]}, 200
        
    except Exception as e:
        logger.error(f"Get user loans error: {str(e)}")
        return {'error': str(e)}, 500


@loans_bp.route('/my-loans/<int:loan_id>', methods=['GET'])
@jwt_required()
def get_user_loan(loan_id):
    """Get specific loan details"""
    try:
        user_id = int(get_jwt_identity())
        loan = Loan.query.filter_by(loan_id=loan_id, user_id=user_id).first()
        
        if not loan:
            return {'error': 'Loan not found'}, 404
        
        return {'loan': loan.to_dict()}, 200
        
    except Exception as e:
        logger.error(f"Get user loan error: {str(e)}")
        return {'error': str(e)}, 500


@loans_bp.route('/my-loans/<int:loan_id>/pre-close', methods=['POST'])
@jwt_required()
def pre_close_loan(loan_id):
    """Request loan pre-closure"""
    try:
        user_id = int(get_jwt_identity())
        loan = Loan.query.filter_by(loan_id=loan_id, user_id=user_id).first()
        
        if not loan:
            return {'error': 'Loan not found'}, 404
        
        if loan.status not in ['Active', 'Approved']:
            return {'error': 'Only active or approved loans can be pre-closed'}, 400
        
        loan.status = 'Closed'
        loan.pre_closure_date = datetime.utcnow()
        
        db.session.commit()
        
        return {
            'message': 'Loan pre-closure requested successfully',
            'loan': loan.to_dict()
        }, 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Pre-close loan error: {str(e)}")
        return {'error': str(e)}, 500






