# Neo Loan Hub - Flask Backend API

A comprehensive Flask-based backend API for the Neo Loan Hub application, providing loan management, user authentication, and administrative features.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **User Management**: Profile management, financial information, and KYC document handling
- **Loan Management**: Loan product browsing, application submission, and status tracking
- **Eligibility Checking**: Automated loan eligibility assessment based on user financial data
- **Admin Panel**: Administrative functions for banks, loan products, and loan approvals
- **File Upload**: Secure KYC document upload and management
- **Database Integration**: MySQL database with SQLAlchemy ORM

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - User registration
- `POST /login` - User login
- `GET /profile` - Get user profile
- `POST /change-password` - Change password
- `GET /verify-token` - Verify JWT token

### User Management (`/api/users`)
- `GET /profile` - Get complete user profile with financial info and KYC docs
- `PUT /profile` - Update user profile
- `GET /financial-info` - Get financial information
- `POST /financial-info` - Create financial information
- `PUT /financial-info` - Update financial information
- `GET /kyc-documents` - Get KYC documents
- `POST /kyc-documents` - Upload KYC document
- `DELETE /kyc-documents/<id>` - Delete KYC document

### Loan Management (`/api/loans`)
- `GET /products` - Get loan products (with filtering)
- `GET /products/<id>` - Get specific loan product
- `POST /apply` - Apply for a loan
- `GET /my-loans` - Get user's loans
- `GET /my-loans/<id>` - Get specific loan details
- `POST /eligibility-check` - Check loan eligibility
- `POST /calculate-emi` - Calculate EMI

### Admin Functions (`/api/admin`)
- `GET /banks` - Get all banks
- `POST /banks` - Create new bank
- `GET /loan-products` - Get all loan products
- `POST /loan-products` - Create loan product
- `PUT /loan-products/<id>` - Update loan product
- `GET /loans` - Get all loans (with filtering)
- `POST /loans/<id>/approve` - Approve loan
- `POST /loans/<id>/reject` - Reject loan
- `GET /kyc-documents` - Get all KYC documents
- `POST /kyc-documents/<id>/verify` - Verify/reject KYC document
- `GET /dashboard/stats` - Get dashboard statistics

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
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DATABASE_URL=mysql+pymysql://username:password@localhost/loan_management_system
   FLASK_ENV=development
   ```

5. **Set up MySQL database**
   - Install MySQL server
   - Create database: `loan_management_system`
   - Run the SQL script from `../database/database.sql`

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Database Schema

The application uses the following main tables:
- `users` - User accounts and profiles
- `financial_info` - User financial information
- `kyc_documents` - KYC document management
- `admin_banks` - Bank information
- `loan_products` - Available loan products
- `loans` - Loan applications and records

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## File Upload

KYC documents can be uploaded as multipart/form-data with the following fields:
- `file`: The document file (PDF, PNG, JPG, JPEG)
- `document_type`: Type of document (e.g., "PAN Card", "Aadhaar Card")
- `document_number`: Document number

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

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Database Migrations
```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

### Testing
Create test files in a `tests/` directory and run with pytest:
```bash
pip install pytest
pytest
```

## Production Deployment

1. **Set production environment variables**
2. **Use a production WSGI server like Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. **Set up reverse proxy with Nginx**
4. **Configure SSL certificates**
5. **Set up database backups**

## Security Considerations

- Change default secret keys in production
- Use HTTPS in production
- Implement rate limiting
- Validate all input data
- Use secure file upload practices
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
