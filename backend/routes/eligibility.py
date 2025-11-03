from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PersonalDetails, FinancialDetails, EmploymentDetails, LoanProduct, Loan
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
eligibility_bp = Blueprint('eligibility', __name__)


@eligibility_bp.route('/check', methods=['POST'])
@jwt_required()
def check_eligibility():
    """Check loan eligibility"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('loan_product_id'):
            return {'error': 'loan_product_id is required'}, 400
        
        # Get user and related data
        user = PersonalDetails.query.get(user_id)
        financial_info = FinancialDetails.query.filter_by(user_id=user_id).first()
        employment_info = EmploymentDetails.query.filter_by(user_id=user_id).first()
        
        if not financial_info or not employment_info:
            return {'error': 'Financial and employment information required'}, 400
        
        # Get loan product
        loan_product = LoanProduct.query.get(data['loan_product_id'])
        if not loan_product:
            return {'error': 'Loan product not found'}, 404
        
        # Eligibility criteria
        eligibility_results = {
            'eligible': True,
            'reasons': [],
            'recommendations': [],
            'maximum_eligible_amount': None
        }
        
        # Check age
        if user.date_of_birth:
            age = (datetime.now().date() - user.date_of_birth).days // 365
            if age < 21:
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Minimum age requirement not met (21 years)')
        
        # Check employment status
        if employment_info.employment_status in ['Unemployed', 'Student']:
            if employment_info.employment_status == 'Student':
                total_income = float(employment_info.monthly_income or 0) + float(employment_info.other_income or 0)
                if total_income < 10000:  # 10k per month minimum
                    eligibility_results['eligible'] = False
                    eligibility_results['reasons'].append('Minimum monthly income not met')
            else:
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append('Unemployed applicants are not eligible')
        
        # Check monthly income
        total_monthly_income = float(employment_info.monthly_income or 0) + float(employment_info.other_income or 0)
        if total_monthly_income < 20000:  # 20k per month minimum
            eligibility_results['eligible'] = False
            eligibility_results['reasons'].append('Monthly income below minimum requirement (₹20,000)')
            eligibility_results['recommendations'].append('Increase your monthly income')
        
        # Check existing loans and debt-to-income ratio
        existing_loans = float(financial_info.existing_loans or 0)
        monthly_emi = float(financial_info.monthly_emi or 0)
        
        if total_monthly_income > 0:
            debt_to_income_ratio = (monthly_emi / total_monthly_income) * 100
            if debt_to_income_ratio > 40:  # 40% threshold
                eligibility_results['eligible'] = False
                eligibility_results['reasons'].append(f'Debt-to-income ratio too high ({debt_to_income_ratio:.1f}%)')
                eligibility_results['recommendations'].append('Reduce existing debt')
        
        # Check active loans count
        active_loans = Loan.query.filter_by(user_id=user_id, status='Active').count()
        if active_loans >= 3:
            eligibility_results['eligible'] = False
            eligibility_results['reasons'].append('Maximum number of active loans reached (3)')
        
        # Calculate recommended loan amount
        if eligibility_results['eligible'] and total_monthly_income > 0:
            # Maximum EMI should be 40% of monthly income
            max_monthly_emi = (total_monthly_income - monthly_emi) * 0.4
            if max_monthly_emi > 0:
                # Calculate maximum loan amount based on EMI
                monthly_rate = loan_product.interest_rate / (12 * 100)
                loan_amount = data.get('loan_amount', loan_product.min_amount)
                tenure_months = data.get('tenure_months', 12)
                
                if tenure_months > 0 and monthly_rate > 0:
                    max_loan_amount = (max_monthly_emi * ((1 + monthly_rate) ** tenure_months - 1)) / \
                                      (monthly_rate * (1 + monthly_rate) ** tenure_months)
                    eligibility_results['maximum_eligible_amount'] = min(
                        max_loan_amount,
                        float(loan_product.max_amount)
                    )
        
        eligibility_results['loan_product'] = loan_product.to_dict()
        
        return eligibility_results, 200
        
    except Exception as e:
        logger.error(f"Check eligibility error: {str(e)}")
        return {'error': str(e)}, 500


@eligibility_bp.route('/calculate-emi', methods=['POST'])
def calculate_emi():
    """Calculate EMI for given loan parameters"""
    try:
        data = request.get_json()
        
        required_fields = ['loan_amount', 'interest_rate', 'tenure_months']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field} is required'}, 400
        
        loan_amount = float(data['loan_amount'])
        interest_rate = float(data['interest_rate'])
        tenure_months = int(data['tenure_months'])
        
        # Calculate EMI using the formula
        monthly_rate = interest_rate / (12 * 100)
        
        if monthly_rate == 0:
            emi = loan_amount / tenure_months
        else:
            emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
                  ((1 + monthly_rate) ** tenure_months - 1)
        
        total_amount = emi * tenure_months
        total_interest = total_amount - loan_amount
        
        return {
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'tenure_months': tenure_months,
            'monthly_emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2)
        }, 200
        
    except Exception as e:
        logger.error(f"Calculate EMI error: {str(e)}")
        return {'error': str(e)}, 500






