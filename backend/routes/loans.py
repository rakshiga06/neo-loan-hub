from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loan, LoanProduct, User, FinancialInfo, KYCDocument
from datetime import datetime
from decimal import Decimal

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/products', methods=['GET'])
def get_loan_products():
    try:
        # Get query parameters for filtering
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
        
        return jsonify({
            'loan_products': [product.to_dict() for product in loan_products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/products/<int:product_id>', methods=['GET'])
def get_loan_product(product_id):
    try:
        loan_product = LoanProduct.query.get(product_id)
        
        if not loan_product:
            return jsonify({'error': 'Loan product not found'}), 404
        
        return jsonify({'loan_product': loan_product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_for_loan():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['loan_product_id', 'loan_amount', 'tenure_months']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if loan product exists
        loan_product = LoanProduct.query.get(data['loan_product_id'])
        if not loan_product:
            return jsonify({'error': 'Loan product not found'}), 404
        
        # Validate loan amount
        loan_amount = Decimal(str(data['loan_amount']))
        if loan_amount < loan_product.min_amount or loan_amount > loan_product.max_amount:
            return jsonify({
                'error': f'Loan amount must be between {loan_product.min_amount} and {loan_product.max_amount}'
            }), 400
        
        # Check if user already has a pending application for this product
        existing_loan = Loan.query.filter_by(
            user_id=user_id,
            loan_product_id=data['loan_product_id'],
            status='Pending'
        ).first()
        
        if existing_loan:
            return jsonify({'error': 'You already have a pending application for this loan product'}), 400
        
        # Create new loan application
        loan = Loan(
            user_id=user_id,
            loan_product_id=data['loan_product_id'],
            loan_amount=loan_amount,
            tenure_months=data['tenure_months'],
            interest_rate=loan_product.interest_rate,
            status='Pending'
        )
        
        db.session.add(loan)
        db.session.commit()
        
        return jsonify({
            'message': 'Loan application submitted successfully',
            'loan': loan.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_user_loans():
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        
        query = Loan.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        loans = query.order_by(Loan.application_date.desc()).all()
        
        return jsonify({
            'loans': [loan.to_dict() for loan in loans]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/my-loans/<int:loan_id>', methods=['GET'])
@jwt_required()
def get_user_loan(loan_id):
    try:
        user_id = get_jwt_identity()
        loan = Loan.query.filter_by(loan_id=loan_id, user_id=user_id).first()
        
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        return jsonify({'loan': loan.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/eligibility-check', methods=['POST'])
@jwt_required()
def check_eligibility():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('loan_product_id'):
            return jsonify({'error': 'loan_product_id is required'}), 400
        
        # Get user and financial info
        user = User.query.get(user_id)
        financial_info = FinancialInfo.query.filter_by(user_id=user_id).first()
        
        if not financial_info:
            return jsonify({'error': 'Financial information not found. Please complete your financial profile.'}), 400
        
        # Get loan product
        loan_product = LoanProduct.query.get(data['loan_product_id'])
        if not loan_product:
            return jsonify({'error': 'Loan product not found'}), 404
        
        # Check KYC status
        kyc_docs = KYCDocument.query.filter_by(user_id=user_id).all()
        kyc_verified = any(doc.status == 'Verified' for doc in kyc_docs)
        
        # Eligibility criteria
        eligibility_results = {
            'eligible': True,
            'reasons': [],
            'recommendations': []
        }
        
        # Check age (assuming minimum age is 21)
        if user.date_of_birth:
            age = (datetime.now().date() - user.date_of_birth).days // 365
            if age < 21:
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Minimum age requirement not met (21 years)')
        
        # Check income
        if financial_info.annual_income:
            if financial_info.annual_income < 200000:  # 2 LPA minimum
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Annual income below minimum requirement (2 LPA)')
        
        # Check credit score
        if financial_info.credit_score:
            if financial_info.credit_score < 600:
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Credit score below minimum requirement (600)')
                eligibility_results['recommendations'].append('Improve your credit score before applying')
        
        # Check debt-to-income ratio
        if financial_info.debt_to_income_ratio:
            if financial_info.debt_to_income_ratio > 0.4:  # 40% threshold
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Debt-to-income ratio too high (above 40%)')
                eligibility_results['recommendations'].append('Reduce existing debt before applying')
        
        # Check KYC verification
        if not kyc_verified:
            eligibility_results['eligible'] = False
            eligibility_results['reasons'].append('KYC documents not verified')
            eligibility_results['recommendations'].append('Complete KYC verification process')
        
        # Check existing loans
        active_loans = Loan.query.filter_by(user_id=user_id, status='Active').count()
        if active_loans >= 3:
            eligibility_results['eligible'] = False
            eligibility_results['reasons'].append('Maximum number of active loans reached (3)')
        
        # Calculate recommended loan amount
        recommended_amount = None
        if financial_info.annual_income and eligibility_results['eligible']:
            # Recommend up to 5 times annual income
            max_recommended = financial_info.annual_income * 5
            recommended_amount = min(max_recommended, float(loan_product.max_amount))
        
        eligibility_results['recommended_amount'] = recommended_amount
        eligibility_results['loan_product'] = loan_product.to_dict()
        
        return jsonify(eligibility_results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/calculate-emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        
        required_fields = ['loan_amount', 'interest_rate', 'tenure_months']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        loan_amount = float(data['loan_amount'])
        interest_rate = float(data['interest_rate'])
        tenure_months = int(data['tenure_months'])
        
        # Calculate EMI using the formula
        monthly_rate = interest_rate / (12 * 100)
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)
        
        total_amount = emi * tenure_months
        total_interest = total_amount - loan_amount
        
        return jsonify({
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'tenure_months': tenure_months,
            'monthly_emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
