from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    financial_info = db.relationship('FinancialInfo', backref='user', uselist=False, cascade='all, delete-orphan')
    kyc_documents = db.relationship('KYCDocument', backref='user', cascade='all, delete-orphan')
    loans = db.relationship('Loan', backref='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class FinancialInfo(db.Model):
    __tablename__ = 'financial_info'
    
    financial_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    employment_status = db.Column(db.String(50))
    annual_income = db.Column(db.Numeric(12, 2))
    credit_score = db.Column(db.Integer)
    existing_loans = db.Column(db.Integer, default=0)
    debt_to_income_ratio = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'user_id': self.user_id,
            'employment_status': self.employment_status,
            'annual_income': float(self.annual_income) if self.annual_income else None,
            'credit_score': self.credit_score,
            'existing_loans': self.existing_loans,
            'debt_to_income_ratio': self.debt_to_income_ratio,
            'last_updated': self.last_updated.isoformat()
        }

class KYCDocument(db.Model):
    __tablename__ = 'kyc_documents'
    
    kyc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    document_type = db.Column(db.String(100))
    document_number = db.Column(db.String(100))
    document_file_path = db.Column(db.String(255))
    status = db.Column(db.Enum('Pending', 'Verified', 'Rejected'), default='Pending', index=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'kyc_id': self.kyc_id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'document_file_path': self.document_file_path,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat(),
            'verified_at': self.verified_at.isoformat() if self.verified_at else None
        }

class AdminBank(db.Model):
    __tablename__ = 'admin_banks'
    
    bank_id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loan_products = db.relationship('LoanProduct', backref='bank', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'bank_id': self.bank_id,
            'bank_name': self.bank_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class LoanProduct(db.Model):
    __tablename__ = 'loan_products'
    
    loan_product_id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('admin_banks.bank_id'), nullable=False, index=True)
    product_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    min_amount = db.Column(db.Numeric(12, 2))
    max_amount = db.Column(db.Numeric(12, 2))
    interest_rate = db.Column(db.Float)
    tenure_range = db.Column(db.String(100))
    eligibility_criteria = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loans = db.relationship('Loan', backref='loan_product', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'loan_product_id': self.loan_product_id,
            'bank_id': self.bank_id,
            'bank_name': self.bank.bank_name if self.bank else None,
            'product_name': self.product_name,
            'description': self.description,
            'min_amount': float(self.min_amount) if self.min_amount else None,
            'max_amount': float(self.max_amount) if self.max_amount else None,
            'interest_rate': self.interest_rate,
            'tenure_range': self.tenure_range,
            'eligibility_criteria': self.eligibility_criteria,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Loan(db.Model):
    __tablename__ = 'loans'
    
    loan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    loan_product_id = db.Column(db.Integer, db.ForeignKey('loan_products.loan_product_id'), nullable=False, index=True)
    loan_amount = db.Column(db.Numeric(12, 2))
    tenure_months = db.Column(db.Integer)
    interest_rate = db.Column(db.Float)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', 'Closed', 'Active'), default='Pending', index=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime)
    disbursal_date = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'user_id': self.user_id,
            'loan_product_id': self.loan_product_id,
            'loan_product_name': self.loan_product.product_name if self.loan_product else None,
            'bank_name': self.loan_product.bank.bank_name if self.loan_product and self.loan_product.bank else None,
            'loan_amount': float(self.loan_amount) if self.loan_amount else None,
            'tenure_months': self.tenure_months,
            'interest_rate': self.interest_rate,
            'status': self.status,
            'application_date': self.application_date.isoformat(),
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'disbursal_date': self.disbursal_date.isoformat() if self.disbursal_date else None
        }
