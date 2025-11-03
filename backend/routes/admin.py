from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loan, LoanProduct, AdminBank, PersonalDetails
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Simple admin check - in production, implement proper role-based access control
        user_id = int(get_jwt_identity())
        user = PersonalDetails.query.get(user_id)
        
        # Check if user is admin (you can add an is_admin field to your User model)
        # For now, checking by email
        if not user or user.email != 'admin@loanhub.com':
            return {'error': 'Admin access required'}, 403
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/loans', methods=['GET'])
@jwt_required()
@admin_required
def get_all_loans():
    """Get all loan applications"""
    try:
        status = request.args.get('status')
        bank_id = request.args.get('bank_id', type=int)
        
        query = Loan.query
        
        if status:
            query = query.filter_by(status=status)
        
        if bank_id:
            query = query.join(LoanProduct).filter(LoanProduct.bank_id == bank_id)
        
        loans = query.order_by(Loan.application_date.desc()).all()
        
        return {'loans': [loan.to_dict() for loan in loans]}, 200
        
    except Exception as e:
        logger.error(f"Get all loans error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/loans/<int:loan_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_loan(loan_id):
    """Approve loan application"""
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return {'error': 'Loan not found'}, 404
        
        if loan.status != 'Pending':
            return {'error': 'Only pending loans can be approved'}, 400
        
        loan.status = 'Approved'
        loan.approval_date = datetime.utcnow()
        
        db.session.commit()
        
        return {
            'message': 'Loan approved successfully',
            'loan': loan.to_dict()
        }, 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Approve loan error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/loans/<int:loan_id>/reject', methods=['POST'])
@jwt_required()
@admin_required
def reject_loan(loan_id):
    """Reject loan application"""
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return {'error': 'Loan not found'}, 404
        
        if loan.status != 'Pending':
            return {'error': 'Only pending loans can be rejected'}, 400
        
        loan.status = 'Rejected'
        loan.approval_date = datetime.utcnow()
        
        db.session.commit()
        
        return {
            'message': 'Loan rejected successfully',
            'loan': loan.to_dict()
        }, 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Reject loan error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/loans/<int:loan_id>/disburse', methods=['POST'])
@jwt_required()
@admin_required
def disburse_loan(loan_id):
    """Disburse approved loan"""
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return {'error': 'Loan not found'}, 404
        
        if loan.status != 'Approved':
            return {'error': 'Only approved loans can be disbursed'}, 400
        
        loan.status = 'Active'
        loan.disbursal_date = datetime.utcnow()
        
        db.session.commit()
        
        return {
            'message': 'Loan disbursed successfully',
            'loan': loan.to_dict()
        }, 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Disburse loan error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
@admin_required
def get_statistics():
    """Get dashboard statistics"""
    try:
        # Total users
        total_users = PersonalDetails.query.count()
        
        # Total loans
        total_loans = Loan.query.count()
        
        # Loans by status
        pending_loans = Loan.query.filter_by(status='Pending').count()
        approved_loans = Loan.query.filter_by(status='Approved').count()
        rejected_loans = Loan.query.filter_by(status='Rejected').count()
        active_loans = Loan.query.filter_by(status='Active').count()
        closed_loans = Loan.query.filter_by(status='Closed').count()
        
        # Total loan amount
        from sqlalchemy import func
        total_loan_amount = db.session.query(func.sum(Loan.loan_amount)).filter_by(status='Active').scalar() or 0
        
        # Total applications this month
        from sqlalchemy import extract
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        monthly_applications = Loan.query.filter(
            extract('month', Loan.application_date) == current_month,
            extract('year', Loan.application_date) == current_year
        ).count()
        
        return {
            'total_users': total_users,
            'total_loans': total_loans,
            'pending_loans': pending_loans,
            'approved_loans': approved_loans,
            'rejected_loans': rejected_loans,
            'active_loans': active_loans,
            'closed_loans': closed_loans,
            'total_loan_amount': float(total_loan_amount),
            'monthly_applications': monthly_applications
        }, 200
        
    except Exception as e:
        logger.error(f"Get statistics error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/banks', methods=['GET'])
@jwt_required()
@admin_required
def get_banks():
    """Get all banks"""
    try:
        banks = AdminBank.query.all()
        return {'banks': [bank.to_dict() for bank in banks]}, 200
    except Exception as e:
        logger.error(f"Get banks error: {str(e)}")
        return {'error': str(e)}, 500


@admin_bp.route('/products', methods=['GET'])
@jwt_required()
@admin_required
def get_all_products():
    """Get all loan products"""
    try:
        loan_products = LoanProduct.query.all()
        return {'loan_products': [product.to_dict() for product in loan_products]}, 200
    except Exception as e:
        logger.error(f"Get products error: {str(e)}")
        return {'error': str(e)}, 500

