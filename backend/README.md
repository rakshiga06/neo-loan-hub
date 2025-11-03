# Banking Loan Management System - Backend API

A secure, scalable Flask-based backend API for the Banking Loan Management System with JWT authentication, OTP verification, and comprehensive loan management features.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **OTP Verification**: Email/Phone OTP verification for user registration and login
- **User Management**: Complete profile, financial, employment, and document management
- **Loan Management**: Loan product browsing, application submission, and status tracking
- **Eligibility Checking**: Automated loan eligibility assessment based on user financial data
- **EMI Calculator**: Calculate loan EMI and total interest
- **Admin Panel**: Administrative functions for loan approvals, analytics, and management
- **File Upload**: Secure document upload and management
- **Database Integration**: MySQL database with SQLAlchemy ORM

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - User registration
- `POST /verify-otp` - Verify OTP
- `POST /resend-otp` - Resend OTP
- `POST /login` - User login
- `GET /verify-token` - Verify JWT token
- `POST /change-password` - Change password

### User Management (`/api/users`)
- `GET /profile` - Get complete user profile
- `PUT /profile` - Update user profile
- `GET /financial-details` - Get financial information
- `POST /financial-details` - Create financial information
- `PUT /financial-details` - Update financial information
- `GET /employment-details` - Get employment information
- `POST /employment-details` - Create employment information
- `PUT /employment-details` - Update employment information
- `GET /documents` - Get user documents
- `POST /upload-document` - Upload document

### Loan Management (`/api/loans`)
- `GET /products` - Get loan products (with filtering)
- `GET /products/<id>` - Get specific loan product
- `POST /apply` - Apply for a loan
- `GET /my-loans` - Get user's loans
- `GET /my-loans/<id>` - Get specific loan details
- `POST /my-loans/<id>/pre-close` - Request loan pre-closure

### Eligibility (`/api/eligibility`)
- `POST /check` - Check loan eligibility
- `POST /calculate-emi` - Calculate EMI

### Admin Functions (`/api/admin`)
- `GET /loans` - Get all loans (with filtering)
- `POST /loans/<id>/approve` - Approve loan
- `POST /loans/<id>/reject` - Reject loan
- `POST /loans/<id>/disburse` - Disburse loan
- `GET /statistics` - Get dashboard statistics
- `GET /banks` - Get all banks
- `GET /products` - Get all loan products

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neo-loan-hub/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DATABASE_URL=mysql+pymysql://username:password@localhost/banking_system
   FLASK_ENV=development
   ```

5. **Set up MySQL database**
   ```bash
   # Run the database schema SQL file
   mysql -u root -p < ../database/database.sql
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Database Schema

The application uses the following main tables:
- `personal_details` - User accounts and profiles
- `financial_details` - User financial information
- `employment_details` - User employment information
- `user_documents` - User document management
- `otp_verifications` - OTP verification records
- `admin_banks` - Bank information
- `loan_products` - Available loan products
- `loans` - Loan applications and records

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## OTP Verification

OTP codes are 6-digit numbers sent to user email/phone. OTPs expire after 10 minutes.

## File Upload

Documents can be uploaded as multipart/form-data with the following fields:
- `file`: The document file (PDF, PNG, JPG, JPEG)
- `document_type`: Type of document (govt_id, address_proof, pan_card, photo)

## Error Handling

The API returns consistent error responses:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Security Considerations

- Change default secret keys in production
- Use HTTPS in production
- Implement rate limiting
- Validate all input data
- Use secure file upload practices
- Regular security updates

## License

MIT License






