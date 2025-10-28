-- ========================================
-- STEP 1: DATABASE SETUP
-- ========================================
-- Copy ALL this code into MySQL
-- Then paste into MySQL query window and execute
-- ========================================

-- Create Database
CREATE DATABASE IF NOT EXISTS loan_management_system;
USE loan_management_system;

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create Financial_Info Table
CREATE TABLE IF NOT EXISTS financial_info (
    financial_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    employment_status VARCHAR(50),
    annual_income DECIMAL(12,2),
    credit_score INT,
    existing_loans INT DEFAULT 0,
    debt_to_income_ratio FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create KYC_Documents Table
CREATE TABLE IF NOT EXISTS kyc_documents (
    kyc_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    document_type VARCHAR(100),
    document_number VARCHAR(100),
    document_file_path VARCHAR(255),
    status ENUM('Pending', 'Verified', 'Rejected') DEFAULT 'Pending',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create Admin_Banks Table
CREATE TABLE IF NOT EXISTS admin_banks (
    bank_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_name VARCHAR(120) NOT NULL UNIQUE,
    contact_email VARCHAR(120),
    contact_phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_bank_name (bank_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create Loan_Products Table
CREATE TABLE IF NOT EXISTS loan_products (
    loan_product_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    product_name VARCHAR(120) NOT NULL,
    description TEXT,
    min_amount DECIMAL(12,2),
    max_amount DECIMAL(12,2),
    interest_rate FLOAT,
    tenure_range VARCHAR(100),
    eligibility_criteria TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bank_id) REFERENCES admin_banks(bank_id) ON DELETE CASCADE,
    INDEX idx_bank_id (bank_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create Loans Table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    loan_product_id INT NOT NULL,
    loan_amount DECIMAL(12,2),
    tenure_months INT,
    interest_rate FLOAT,
    status ENUM('Pending', 'Approved', 'Rejected', 'Closed', 'Active') DEFAULT 'Pending',
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approval_date TIMESTAMP NULL,
    disbursal_date TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (loan_product_id) REFERENCES loan_products(loan_product_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_loan_product_id (loan_product_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Sample Banks
INSERT INTO admin_banks (bank_name, contact_email, contact_phone, address) VALUES
('HDFC Bank', 'hdfc@bank.com', '+91-8888-888-888', 'HDFC Towers, Mumbai, India'),
('ICICI Bank', 'icici@bank.com', '+91-8787-878-787', 'ICICI Tower, Delhi, India'),
('SBI Bank', 'sbi@bank.com', '+91-8686-868-686', 'SBI Tower, Chennai, India'),
('Axis Bank', 'axis@bank.com', '+91-8585-858-585', 'Axis Tower, Bangalore, India'),
('Kotak Bank', 'kotak@bank.com', '+91-8484-848-484', 'Kotak Tower, Hyderabad, India');

-- Insert Sample Loan Products
INSERT INTO loan_products (bank_id, product_name, description, min_amount, max_amount, interest_rate, tenure_range, eligibility_criteria) VALUES
(1, 'Personal Loan', 'Flexible personal loans with quick approval', 100000, 5000000, 7.5, '12-60 months', 'Min age 21, Income 3 LPA'),
(1, 'Home Loan', 'Competitive home loan rates', 500000, 50000000, 6.5, '60-300 months', 'Min age 25, Income 5 LPA'),
(2, 'Auto Loan', 'Easy auto financing solutions', 200000, 3000000, 8.0, '24-84 months', 'Min age 23, Income 2.5 LPA'),
(2, 'Education Loan', 'Special rates for education', 100000, 2000000, 6.0, '60-120 months', 'Student with admission letter'),
(3, 'Business Loan', 'For business expansion and working capital', 500000, 10000000, 9.0, '36-72 months', 'Business owner with 2 years experience'),
(3, 'Personal Loan', 'Quick disbursal personal loans', 50000, 3000000, 8.5, '6-60 months', 'Min age 18, Income 2 LPA'),
(4, 'Home Loan', 'Best home loan rates in market', 750000, 75000000, 6.0, '84-360 months', 'Min age 25, Income 6 LPA'),
(5, 'Investment Loan', 'For investment purposes', 300000, 5000000, 7.0, '24-60 months', 'Income 4 LPA');

-- Verify tables created
SHOW TABLES;
DESCRIBE users;
DESCRIBE financial_info;
DESCRIBE kyc_documents;
DESCRIBE admin_banks;
DESCRIBE loan_products;
DESCRIBE loans;