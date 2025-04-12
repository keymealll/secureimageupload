# Secure Image Uploading Web Application

## Overview

This project is a web application that allows users to securely upload, store, and manage image files. It includes user authentication, secure image upload with validation, encrypted storage, and a personal gallery for each user.

## Security Features

### User Authentication
- Secure password handling using Django's authentication system with bcrypt
- Custom password requirements: 12+ characters, upper/lowercase, numbers, special characters
- Email verification for new accounts
- Rate limiting on login attempts
- Account lockout after multiple failed attempts
- CSRF protection on all forms

### Secure Image Upload
- Comprehensive file validation:
  - MIME type checking using python-magic
  - Content verification with PIL/Pillow
  - Image dimension validation to prevent DoS attacks
  - File size limits (5MB max)
- Sanitization of filenames and metadata
- Random UUID-based filenames to prevent path traversal
- Whitelisting of allowed image formats (.jpg, .png, .gif)

### Secure Storage
- AES-256-CBC encryption for all stored images
- Separation of encrypted data and encryption keys
- Secure key management (session-based in this demo, would use HSM or KMS in production)

### Access Control
- Users can only access their own images
- Proper authorization checks on all image operations
- HTTP security headers (CSP, X-Frame-Options, etc.)

### Secure Configuration
- HTTPS enforcement
- Secure cookie settings
- HSTS implementation
- Restrictive Content Security Policy

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or MySQL
- Virtual environment tool (virtualenv or venv)

### Installation Steps

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd secure-image-app
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secure_random_key
   DEBUG=False
   DATABASE_URL=postgres://user:password@localhost/dbname
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

5. Run database migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Run the server
   ```bash
   python manage.py runserver
   ```

## Architecture

### Component Overview
```
┌────────────────────────┐
│     User Interface     │
│  (HTML, CSS, JS, Forms)│
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│  Django Web Framework  │
│    (Views, Templates)  │
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│   Security Middleware  │
│ (CSRF, Auth, Validation)│
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│ Image Processing/Crypto│
│ (Validation, Encryption)│
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│    Database Storage    │
│  (PostgreSQL/MySQL)    │
└────────────────────────┘
```

### 🔧 Core Technologies
- 🐍 **Backend**: Django (Python)
- 💾 **Database**: PostgreSQL (recommended)
- 🔑 **Authentication**: Django Authentication System + Custom Extensions
- 🔐 **Encryption**: AES-256-CBC via Python Cryptography library
- ✅ **File Validation**: python-magic, Pillow, custom validators
- 🎨 **Frontend**: HTML, CSS, JavaScript, Bootstrap

## 🤔 Development Decisions and Tradeoffs

### 🔒 Encryption Implementation
We chose AES-256-CBC for image encryption due to its security and efficiency balance. In a production environment, keys should be stored in a separate secure database or HSM.

### 📦 Storage Strategy
We store encrypted image data directly in the database as binary fields. For a production system with many or large images, consider:
- Storing encrypted images on a filesystem with proper permissions
- Using a secure object storage service (like S3 with server-side encryption)
- Implementing a dedicated secure file storage system

### 🔐 Session Management
In this implementation, encryption keys are stored in the session for simplicity. In a production environment:
- Use a proper key management system (KMS)
- Consider a hardware security module (HSM) for key protection
- Implement a more robust key rotation and management strategy

## Security Testing

The application includes security tests covering:
- Authentication and authorization
- CSRF protection
- File upload validation
- Access control enforcement
- Password policy enforcement
- Rate limiting

## Potential Improvements

1. **Advanced Encryption Features**
   - Implement key rotation
   - Add per-user encryption keys
   - Use a proper key management system

2. **Additional Authentication Security**
   - Complete multi-factor authentication implementation
   - OAuth integration for third-party login

3. **Enhanced Image Protection**
   - Add watermarking capabilities
   - Implement download restrictions
   - Add image metadata stripping

4. **Monitoring and Logging**
   - Comprehensive security event logging
   - Intrusion detection system
   - Real-time security alerts

5. **Performance Optimizations**
   - Image caching for faster retrieval
   - Thumbnail generation for gallery view
   - Background processing for encryption/decryption of large files

## Assumptions

- The application is meant to be deployed over HTTPS
- A proper database backup strategy will be implemented
- The system will be kept updated with security patches
- The server environment will be properly hardened
- Access to server and database will be restricted and secured