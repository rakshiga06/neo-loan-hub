
-- Database: banking_system
CREATE DATABASE IF NOT EXISTS banking_system;
USE banking_system;

-- ======================
-- 1️⃣ PERSONAL DETAILS
-- ======================
CREATE TABLE personal_details (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    marital_status ENUM('Single', 'Married', 'Divorced', 'Widowed') NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    permanent_address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- 2️⃣ FINANCIAL DETAILS
-- ======================
CREATE TABLE financial_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    existing_loans DECIMAL(15,2) DEFAULT 0,
    monthly_emi DECIMAL(15,2) DEFAULT 0,
    assets_owned TEXT,
    bank_account_details TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES personal_details(user_id) ON DELETE CASCADE
);

-- ======================
-- 3️⃣ EMPLOYMENT DETAILS
-- ======================
CREATE TABLE employment_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    employment_status ENUM('Employed', 'Self-employed', 'Unemployed', 'Student') NOT NULL,
    employer_name_address TEXT,
    job_title VARCHAR(100),
    monthly_income DECIMAL(15,2) NOT NULL,
    other_income DECIMAL(15,2),
    income_proof_path VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES personal_details(user_id) ON DELETE CASCADE
);

-- ======================
-- 4️⃣ USER DOCUMENTS
-- ======================
CREATE TABLE user_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    govt_id_path VARCHAR(255),
    address_proof_path VARCHAR(255),
    pan_card_path VARCHAR(255),
    photo_path VARCHAR(255),
    other_docs_path VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES personal_details(user_id) ON DELETE CASCADE
);
