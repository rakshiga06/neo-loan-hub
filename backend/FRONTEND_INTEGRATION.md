# Frontend-Backend Integration Guide

This document explains how the frontend should call the backend API endpoints.

## Base URL
```
http://localhost:5000/api
```

## Field Naming Convention

**All field names match between frontend and backend** using **camelCase**.

### Frontend Form Fields → Backend API Fields

#### Personal Details
- `full_name` → `full_name`
- `dob` → `date_of_birth` (format: YYYY-MM-DD)
- `gender` → `gender`
- `nationality` → `nationality`
- `maritalStatus` → `marital_status`
- `contact` → `contact_number`
- `email` → `email`
- `password` → `password`
- `confirmPassword` → (not sent to backend, frontend validation only)
- `address` → `permanent_address`

#### Financial Details
- `existingLoans` → `existing_loans`
- `monthlyEMI` → `monthly_emi`
- `assets` → `assets_owned`
- `bankDetails` → `bank_account_details`

#### Employment Details
- `employmentStatus` → `employment_status`
- `employerName` → `employer_name_address`
- `jobTitle` → `job_title`
- `income` → `monthly_income`
- `otherIncome` → `other_income`

---

## Complete API Flow

### 1. User Registration with OTP

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "contact_number": "9999999999",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "nationality": "Indian",
  "marital_status": "Single",
  "permanent_address": "123 Main Street, City"
}
```

**Response:**
```json
{
  "message": "User registered successfully. OTP sent to email.",
  "user_id": 1,
  "requires_otp_verification": true
}
```

### 2. Verify OTP

**Endpoint:** `POST /api/auth/verify-otp`

**Request Body:**
```json
{
  "user_id": 1,
  "otp_code": "123456",
  "otp_type": "email"
}
```

**Response:**
```json
{
  "message": "OTP verified successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { ... }
}
```

### 3. Login

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { ... }
}
```

### 4. Save Personal Details (Protected)

**Endpoint:** `PUT /api/users/profile`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John Doe Updated",
  "contact_number": "9999999999",
  "permanent_address": "Updated address"
}
```

### 5. Save Financial Details (Protected)

**Endpoint:** `POST /api/users/financial-details`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "existing_loans": 500000,
  "monthly_emi": 25000,
  "assets_owned": "House, Car",
  "bank_account_details": "Account: 1234567890, IFSC: ABC0123456"
}
```

### 6. Save Employment Details (Protected)

**Endpoint:** `POST /api/users/employment-details`

**Request Body:**
```json
{
  "employment_status": "Employed",
  "employer_name_address": "Tech Corp, Bangalore",
  "job_title": "Software Engineer",
  "monthly_income": 75000,
  "other_income": 10000
}
```

### 7. Upload Documents (Protected)

**Endpoint:** `POST /api/users/upload-document`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: (binary file)
- `document_type`: `govt_id`, `address_proof`, `pan_card`, or `photo`

### 8. Check Eligibility (Protected)

**Endpoint:** `POST /api/eligibility/check`

**Request Body:**
```json
{
  "loan_product_id": 1
}
```

**Response:**
```json
{
  "eligible": true,
  "reasons": [],
  "recommendations": [],
  "maximum_eligible_amount": 2000000,
  "loan_product": { ... }
}
```

### 9. Calculate EMI

**Endpoint:** `POST /api/eligibility/calculate-emi`

**Request Body:**
```json
{
  "loan_amount": 500000,
  "interest_rate": 8.5,
  "tenure_months": 24
}
```

**Response:**
```json
{
  "loan_amount": 500000,
  "interest_rate": 8.5,
  "tenure_months": 24,
  "monthly_emi": 22727.84,
  "total_amount": 545468.1,
  "total_interest": 45468.1
}
```

### 10. Apply for Loan (Protected)

**Endpoint:** `POST /api/loans/apply`

**Request Body:**
```json
{
  "loan_product_id": 1,
  "loan_amount": 500000,
  "tenure_months": 24
}
```

---

## Frontend Integration Example

### Registration Flow

```typescript
// Step 1: Register
const registerResponse = await fetch('http://localhost:5000/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    full_name: formData.fullName,
    email: formData.email,
    password: formData.password,
    contact_number: formData.contact,
    date_of_birth: formData.dob,
    gender: formData.gender,
    nationality: formData.nationality,
    marital_status: formData.maritalStatus,
    permanent_address: formData.address
  })
});
const registerData = await registerResponse.json();

// Step 2: Verify OTP (from server logs in dev)
const otpResponse = await fetch('http://localhost:5000/api/auth/verify-otp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_id: registerData.user_id,
    otp_code: otpCodeFromUser,
    otp_type: 'email'
  })
});
const otpData = await otpResponse.json();

// Store token
localStorage.setItem('token', otpData.access_token);
```

### Saving Form Data

```typescript
// Save personal details
const token = localStorage.getItem('token');
await fetch('http://localhost:5000/api/users/profile', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    full_name: formData.fullName,
    contact_number: formData.contact,
    permanent_address: formData.address
  })
});

// Save financial details
await fetch('http://localhost:5000/api/users/financial-details', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    existing_loans: parseFloat(formData.existingLoans) || 0,
    monthly_emi: parseFloat(formData.monthlyEMI) || 0,
    assets_owned: formData.assets,
    bank_account_details: formData.bankDetails
  })
});

// Save employment details
await fetch('http://localhost:5000/api/users/employment-details', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    employment_status: formData.employmentStatus,
    employer_name_address: formData.employerName,
    job_title: formData.jobTitle,
    monthly_income: parseFloat(formData.income) || 0,
    other_income: parseFloat(formData.otherIncome) || 0
  })
});
```

---

## Testing

Use the following curl commands to test the API:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","email":"test@test.com","password":"Test1234","contact_number":"9999999999","date_of_birth":"1990-01-01","gender":"Male","nationality":"Indian","marital_status":"Single","permanent_address":"Test"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test1234"}'

# Get loan products
curl http://localhost:5000/api/loans/products
```

---

## Notes

1. **Token Storage:** Store the `access_token` in localStorage or secure storage
2. **Date Format:** Always send dates as `YYYY-MM-DD` strings
3. **Error Handling:** All errors return `{"error": "message"}`
4. **File Uploads:** Documents are uploaded as multipart/form-data
5. **OTP Testing:** In development, check server logs for OTP codes






