# 🔐 Login Authentication System

## Python + MySQL Project Specification

------------------------------------------------------------------------

# 1️⃣ Project Overview

**Project Name:**\
Login Authentication System (Python + MySQL)

**Goal:**\
To build a secure, scalable, and modular login authentication system
with registration, login, password recovery, and role-based access
control.

**Target Users:**\
- Admin\
- Staff\
- General Users

**Platform:**\
(Tkinter Desktop / Flask Web / CLI -- update as needed)

**Environment:**\
- Windows 10/11\
- Python 3.x\
- MySQL 8.x

------------------------------------------------------------------------

# 2️⃣ Tech Stack & Constraints

**Backend:** Python\
**Database:** MySQL\
**Database Connector:** mysql-connector-python / pymysql\
**Password Hashing:** bcrypt\
**Architecture:** Modular

**Security Requirements:**\
- Password must be hashed (bcrypt)\
- No plain-text passwords stored\
- Parameterized SQL queries only\
- Basic input validation

------------------------------------------------------------------------

# 3️⃣ Authentication Features

## Core Features

-   User Registration\
-   User Login\
-   Logout (if web)\
-   Password Hashing\
-   Unique Email / Username\
-   Role-Based Access

## Account Recovery

-   Forgot Password (OTP-based or token-based reset)\
-   Reset Password

## Security Controls

-   Account lock after 5 failed login attempts\
-   Login attempt logging\
-   Role-based access control (RBAC)\
-   Password complexity validation

------------------------------------------------------------------------

# 4️⃣ User Roles & Permissions

## Admin

-   View all users\
-   Approve or deactivate users\
-   Reset user passwords\
-   View login history

## Staff

-   Limited dashboard access

## General User

-   Register\
-   Login\
-   Reset password\
-   View own profile

------------------------------------------------------------------------

# 5️⃣ Database Design (MySQL)

## Table: users

-   id (INT, PK, AUTO_INCREMENT)\
-   full_name (VARCHAR(100), NOT NULL)\
-   email (VARCHAR(150), UNIQUE, NOT NULL)\
-   mobile (VARCHAR(15), UNIQUE)\
-   password_hash (VARCHAR(255), NOT NULL)\
-   role (VARCHAR(50), DEFAULT 'user')\
-   status (ENUM('active','inactive','locked'), DEFAULT 'active')\
-   failed_attempts (INT, DEFAULT 0)\
-   created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)\
-   last_login (TIMESTAMP, NULL)

------------------------------------------------------------------------

## Table: login_attempts

-   id (INT, PK, AUTO_INCREMENT)\
-   user_id (INT, FK)\
-   attempt_time (TIMESTAMP)\
-   status (VARCHAR(20))\
-   ip_address (VARCHAR(50))

------------------------------------------------------------------------

## Table: password_reset_tokens

-   id (INT, PK)\
-   user_id (INT, FK)\
-   token (VARCHAR(255))\
-   expires_at (TIMESTAMP)\
-   used (BOOLEAN)

------------------------------------------------------------------------

# 6️⃣ User Workflows

## Registration Flow

1.  User enters details\
2.  Validate input\
3.  Hash password using bcrypt\
4.  Insert into database\
5.  Show success message

## Login Flow

1.  User enters credentials\
2.  Compare hashed password\
3.  Handle failed attempts\
4.  Lock account if limit exceeded

## Forgot Password Flow

1.  Generate secure token\
2.  Store token\
3.  Allow reset within expiry\
4.  Update hashed password

------------------------------------------------------------------------

# 7️⃣ UI Requirements

-   Login Screen\
-   Registration Screen\
-   Forgot Password Screen\
-   Dashboard\
-   Admin Panel\
-   Show/Hide password toggle\
-   Proper error messages

------------------------------------------------------------------------

# 8️⃣ Validation Rules

-   Minimum 8-character password\
-   Must include uppercase, lowercase, number\
-   Valid email format\
-   10-digit mobile number\
-   No empty fields

------------------------------------------------------------------------

# 9️⃣ Folder Structure

login_auth_project/ │ ├── main.py\
├── config.py\
├── db.py\
├── auth.py\
├── models.py\
├── utils.py\
├── ui/\
├── templates/\
└── README.md

------------------------------------------------------------------------

# 🔟 Setup Instructions

1.  Install Python\
2.  Install MySQL\
3.  Create database\
4.  Run DDL scripts\
5.  Install dependencies:

pip install mysql-connector-python bcrypt

6.  Configure DB credentials\
7.  Run main.py

------------------------------------------------------------------------

# Future Enhancements

-   Two-Factor Authentication (2FA)\
-   Email verification\
-   JWT authentication\
-   OAuth login\
-   Docker deployment

------------------------------------------------------------------------

**End of Specification**
