# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

# db = SQLAlchemy()

# class PersonalDetails(db.Model):
#     """User Personal Details Table"""
#     __tablename__ = 'personal_details'
    
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
#     nationality = db.Column(db.String(50), nullable=False)
#     marital_status = db.Column(db.Enum('Single', 'Married', 'Divorced', 'Widowed'), nullable=False)
#     contact_number = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False, index=True)
#     password_hash = db.Column(db.String(255), nullable=False)
#     permanent_address = db.Column(db.Text, nullable=False)
#     is_email_verified = db.Column(db.Boolean, default=False)
#     is_phone_verified = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationships
#     financial_details = db.relationship('FinancialDetails', backref='user', uselist=False, cascade='all, delete-orphan')
#     employment_details = db.relationship('EmploymentDetails', backref='user', uselist=False, cascade='all, delete-orphan')
#     user_documents = db.relationship('UserDocuments', backref='user', uselist=False, cascade='all, delete-orphan')
#     otp_verifications = db.relationship('OTPVerification', backref='user', cascade='all, delete-orphan')
#     loans = db.relationship('Loan', backref='user', cascade='all, delete-orphan')
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'full_name': self.full_name,
#             'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
#             'gender': self.gender,
#             'nationality': self.nationality,
#             'marital_status': self.marital_status,
#             'contact_number': self.contact_number,
#             'email': self.email,
#             'permanent_address': self.permanent_address,
#             'is_email_verified': self.is_email_verified,
#             'is_phone_verified': self.is_phone_verified,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }


# class FinancialDetails(db.Model):
#     """User Financial Details Table"""
#     __tablename__ = 'financial_details'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
#     existing_loans = db.Column(db.Numeric(15, 2), default=0)
#     monthly_emi = db.Column(db.Numeric(15, 2), default=0)
#     assets_owned = db.Column(db.Text)
#     bank_account_details = db.Column(db.Text, nullable=False)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'existing_loans': float(self.existing_loans) if self.existing_loans else 0,
#             'monthly_emi': float(self.monthly_emi) if self.monthly_emi else 0,
#             'assets_owned': self.assets_owned,
#             'bank_account_details': self.bank_account_details
#         }


# class EmploymentDetails(db.Model):
#     """User Employment Details Table"""
#     __tablename__ = 'employment_details'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
#     employment_status = db.Column(db.Enum('Employed', 'Self-employed', 'Unemployed', 'Student'), nullable=False)
#     employer_name_address = db.Column(db.Text)
#     job_title = db.Column(db.String(100))
#     monthly_income = db.Column(db.Numeric(15, 2), nullable=False)
#     other_income = db.Column(db.Numeric(15, 2), default=0)
#     income_proof_path = db.Column(db.String(255))
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'employment_status': self.employment_status,
#             'employer_name_address': self.employer_name_address,
#             'job_title': self.job_title,
#             'monthly_income': float(self.monthly_income) if self.monthly_income else 0,
#             'other_income': float(self.other_income) if self.other_income else 0,
#             'income_proof_path': self.income_proof_path
#         }


# class UserDocuments(db.Model):
#     """User Documents Table"""
#     __tablename__ = 'user_documents'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
#     govt_id_path = db.Column(db.String(255))
#     address_proof_path = db.Column(db.String(255))
#     pan_card_path = db.Column(db.String(255))
#     photo_path = db.Column(db.String(255))
#     other_docs_path = db.Column(db.String(255))
#     uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'govt_id_path': self.govt_id_path,
#             'address_proof_path': self.address_proof_path,
#             'pan_card_path': self.pan_card_path,
#             'photo_path': self.photo_path,
#             'other_docs_path': self.other_docs_path,
#             'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
#         }


# class OTPVerification(db.Model):
#     """OTP Verification Table"""
#     __tablename__ = 'otp_verifications'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False)
#     otp_code = db.Column(db.String(6), nullable=False)
#     otp_type = db.Column(db.Enum('email', 'phone'), nullable=False)
#     expires_at = db.Column(db.DateTime, nullable=False)
#     is_verified = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def is_expired(self):
#         return datetime.utcnow() > self.expires_at


# class LoanProduct(db.Model):
#     """Loan Products Table"""
#     __tablename__ = 'loan_products'
    
#     loan_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     bank_id = db.Column(db.Integer, db.ForeignKey('admin_banks.bank_id'), nullable=False)
#     product_name = db.Column(db.String(120), nullable=False)
#     description = db.Column(db.Text)
#     min_amount = db.Column(db.Numeric(12, 2))
#     max_amount = db.Column(db.Numeric(12, 2))
#     interest_rate = db.Column(db.Float)
#     tenure_range = db.Column(db.String(100))
#     eligibility_criteria = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     bank = db.relationship('AdminBank', backref='loan_products')
#     loans = db.relationship('Loan', backref='loan_product', cascade='all, delete-orphan')
    
#     def to_dict(self):
#         return {
#             'loan_product_id': self.loan_product_id,
#             'bank_id': self.bank_id,
#             'bank_name': self.bank.bank_name if self.bank else None,
#             'product_name': self.product_name,
#             'description': self.description,
#             'min_amount': float(self.min_amount) if self.min_amount else None,
#             'max_amount': float(self.max_amount) if self.max_amount else None,
#             'interest_rate': self.interest_rate,
#             'tenure_range': self.tenure_range,
#             'eligibility_criteria': self.eligibility_criteria,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None
#         }


# class AdminBank(db.Model):
#     """Admin Banks Table"""
#     __tablename__ = 'admin_banks'
    
#     bank_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     bank_name = db.Column(db.String(120), nullable=False, unique=True)
#     contact_email = db.Column(db.String(120))
#     contact_phone = db.Column(db.String(20))
#     address = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     def to_dict(self):
#         return {
#             'bank_id': self.bank_id,
#             'bank_name': self.bank_name,
#             'contact_email': self.contact_email,
#             'contact_phone': self.contact_phone,
#             'address': self.address,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None
#         }


# class Loan(db.Model):
#     """Loans Table"""
#     __tablename__ = 'loans'
    
#     loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False)
#     loan_product_id = db.Column(db.Integer, db.ForeignKey('loan_products.loan_product_id'), nullable=False)
#     loan_amount = db.Column(db.Numeric(12, 2))
#     tenure_months = db.Column(db.Integer)
#     interest_rate = db.Column(db.Float)
#     monthly_emi = db.Column(db.Numeric(15, 2))
#     status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', 'Closed', 'Active'), default='Pending', index=True)
#     application_date = db.Column(db.DateTime, default=datetime.utcnow)
#     approval_date = db.Column(db.DateTime)
#     disbursal_date = db.Column(db.DateTime)
#     pre_closure_date = db.Column(db.DateTime)
    
#     def to_dict(self):
#         return {
#             'loan_id': self.loan_id,
#             'user_id': self.user_id,
#             'loan_product_id': self.loan_product_id,
#             'product_name': self.loan_product.product_name if self.loan_product else None,
#             'bank_name': self.loan_product.bank.bank_name if self.loan_product and self.loan_product.bank else None,
#             'loan_amount': float(self.loan_amount) if self.loan_amount else None,
#             'tenure_months': self.tenure_months,
#             'interest_rate': self.interest_rate,
#             'monthly_emi': float(self.monthly_emi) if self.monthly_emi else None,
#             'status': self.status,
#             'application_date': self.application_date.isoformat() if self.application_date else None,
#             'approval_date': self.approval_date.isoformat() if self.approval_date else None,
#             'disbursal_date': self.disbursal_date.isoformat() if self.disbursal_date else None,
#             'pre_closure_date': self.pre_closure_date.isoformat() if self.pre_closure_date else None
#         }
    



from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class PersonalDetails(db.Model):
    """User Personal Details Table"""
    __tablename__ = 'personal_details'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    marital_status = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    permanent_address = db.Column(db.Text, nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    financial_details = db.relationship('FinancialDetails', backref='user', uselist=False, cascade='all, delete-orphan')
    employment_details = db.relationship('EmploymentDetails', backref='user', uselist=False, cascade='all, delete-orphan')
    user_documents = db.relationship('UserDocuments', backref='user', uselist=False, cascade='all, delete-orphan')
    otp_verifications = db.relationship('OTPVerification', backref='user', cascade='all, delete-orphan')
    loans = db.relationship('Loan', backref='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'nationality': self.nationality,
            'marital_status': self.marital_status,
            'contact_number': self.contact_number,
            'email': self.email,
            'permanent_address': self.permanent_address,
            'is_email_verified': self.is_email_verified,
            'is_phone_verified': self.is_phone_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FinancialDetails(db.Model):
    """User Financial Details Table"""
    __tablename__ = 'financial_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
    existing_loans = db.Column(db.Numeric(15, 2), default=0)
    monthly_emi = db.Column(db.Numeric(15, 2), default=0)
    assets_owned = db.Column(db.Text)
    bank_account_details = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'existing_loans': float(self.existing_loans) if self.existing_loans else 0,
            'monthly_emi': float(self.monthly_emi) if self.monthly_emi else 0,
            'assets_owned': self.assets_owned,
            'bank_account_details': self.bank_account_details
        }


class EmploymentDetails(db.Model):
    """User Employment Details Table"""
    __tablename__ = 'employment_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
    employment_status = db.Column(db.Enum('Employed', 'Self-employed', 'Unemployed', 'Student'), nullable=False)
    employer_name_address = db.Column(db.Text)
    job_title = db.Column(db.String(100))
    monthly_income = db.Column(db.Numeric(15, 2), nullable=False)
    other_income = db.Column(db.Numeric(15, 2), default=0)
    income_proof_path = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employment_status': self.employment_status,
            'employer_name_address': self.employer_name_address,
            'job_title': self.job_title,
            'monthly_income': float(self.monthly_income) if self.monthly_income else 0,
            'other_income': float(self.other_income) if self.other_income else 0,
            'income_proof_path': self.income_proof_path
        }


class UserDocuments(db.Model):
    """User Documents Table"""
    __tablename__ = 'user_documents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False, unique=True)
    govt_id_path = db.Column(db.String(255))
    address_proof_path = db.Column(db.String(255))
    pan_card_path = db.Column(db.String(255))
    photo_path = db.Column(db.String(255))
    other_docs_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'govt_id_path': self.govt_id_path,
            'address_proof_path': self.address_proof_path,
            'pan_card_path': self.pan_card_path,
            'photo_path': self.photo_path,
            'other_docs_path': self.other_docs_path,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class OTPVerification(db.Model):
    """OTP Verification Table"""
    __tablename__ = 'otp_verifications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    otp_type = db.Column(db.Enum('email', 'phone'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at


class LoanProduct(db.Model):
    """Loan Products Table"""
    __tablename__ = 'loan_products'
    
    loan_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('admin_banks.bank_id'), nullable=False)
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
    bank = db.relationship('AdminBank', backref='loan_products')
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AdminBank(db.Model):
    """Admin Banks Table"""
    __tablename__ = 'admin_banks'
    
    bank_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(120), nullable=False, unique=True)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'bank_id': self.bank_id,
            'bank_name': self.bank_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Loan(db.Model):
    """Loans Table"""
    __tablename__ = 'loans'
    
    loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_details.user_id'), nullable=False)
    loan_product_id = db.Column(db.Integer, db.ForeignKey('loan_products.loan_product_id'), nullable=False)
    loan_amount = db.Column(db.Numeric(12, 2))
    tenure_months = db.Column(db.Integer)
    interest_rate = db.Column(db.Float)
    monthly_emi = db.Column(db.Numeric(15, 2))
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', 'Closed', 'Active'), default='Pending', index=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime)
    disbursal_date = db.Column(db.DateTime)
    pre_closure_date = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'user_id': self.user_id,
            'loan_product_id': self.loan_product_id,
            'product_name': self.loan_product.product_name if self.loan_product else None,
            'bank_name': self.loan_product.bank.bank_name if self.loan_product and self.loan_product.bank else None,
            'loan_amount': float(self.loan_amount) if self.loan_amount else None,
            'tenure_months': self.tenure_months,
            'interest_rate': self.interest_rate,
            'monthly_emi': float(self.monthly_emi) if self.monthly_emi else None,
            'status': self.status,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'disbursal_date': self.disbursal_date.isoformat() if self.disbursal_date else None,
            'pre_closure_date': self.pre_closure_date.isoformat() if self.pre_closure_date else None
        }




