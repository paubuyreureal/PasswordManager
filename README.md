# Password Manager

Secure web application for managing passwords and credentials, built with Django REST Framework on the backend and React on the frontend, fully containerized with Docker and deployed on GitHub Codespaces.

## 🚀 Demo

**Access the application directly:** [Open in GitHub Codespaces](https://github.com/paubuyreureal/PasswordManager)

The application is fully functional and ready to test with:
- User registration and authentication
- Secure password storage with encryption
- Password recovery functionality (email in console)
- Search and filtering capabilities

## 🛠️ Tech Stack

### Backend
- **Python 3.9** with **Django 4.2** and **Django REST Framework**
- **PostgreSQL** as the main database
- **JWT Authentication** with refresh tokens
- **AES Encryption** for stored passwords
- **bcrypt** for user password hashing

### Frontend
- **React 18** with **Vite** as build tool
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API communication

### Infrastructure
- **Docker** and **Docker Compose** for containerization
- **GitHub Codespaces** for cloud deployment
- **Nginx** as reverse proxy and static file server
- **DevContainer** configured for frictionless development

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│────│  Nginx Proxy    │────│ Django Backend  │
│   (Port 3000)   │    │   (Port 80)     │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                               ┌─────────────────┐
                                               │   PostgreSQL    │
                                               │   (Port 5432)   │
                                               └─────────────────┘
```

## 🚀 Setup

### GitHub Codespaces

1. **Click the "Code" button** in this repository
2. **Select "Codespaces"** → **"Create codespace on main"**
3. **Wait several minutes** for automatic setup (dependencies are installed automatically, wait until the terminal allows user input)
4. **Access the application** on the forwarded port (usually port 3000)

## 📋 Environment Variables

The application uses the `codespaces.env` file for configuration in Codespaces. For reference, check `docker.env.example` which contains the template for all necessary variables:

- **Email configuration** (for password recovery) --- NOT USED IN CURRENT VERSION
- **Django configuration** (SECRET_KEY, DEBUG, etc.)
- **Database** (automatically configured in Docker)

## 🔌 API Endpoints (Test through Frontend)

### Authentication
```bash
# User registration
POST /api/register/
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword"
}

# Login
POST /api/login/
{
  "username": "testuser",
  "password": "securepassword"
}

# Password reset request
POST /api/password-reset/
{
  "username": "testuser"
}

# Password reset confirmation
POST /api/password-reset/confirm/
{
  "token": "reset-token",
  "password": "newpassword"
}
```

### Password Management (Requires Authentication)
```bash
# Get all accounts
GET /api/accounts/

# Create new account
POST /api/accounts/
{
  "username": "gmail_user",
  "password": "gmail_password",
  "url": "https://gmail.com",
  "notes": "Personal email account"
}

# Update account
PUT /api/accounts/{id}/
{
  "username": "updated_user",
  "password": "new_password",
  "url": "https://updated-site.com"
}

# Delete account
DELETE /api/accounts/{id}/

# Search accounts
GET /api/accounts/?search=gmail
GET /api/accounts/?url_filter=google.com
```

## 🔄 Password Recovery Functionality

**Important:** In the current version, no real email is sent. Instead, the email content is printed to the backend logs where you can access the password reset link. For this feature, access the logs through Codespaces.

### How it works:

1. **User requests recovery:** Enter their username
2. **Backend generates link:** A secure token is created and the link is generated
3. **Email is printed to logs:** The complete email content appears in the backend logs
4. **Access logs:** To view the email and link:
   ```bash
   docker compose -f docker-compose.codespaces.yml logs -f backend
   ```
   or in the **Containers** section, right-click on the Backend container and select **View Logs**
5. **Use the link:** Copy the link from the logs and open it in the browser to reset the password

This implementation allows testing the complete functionality without needing to configure a real email server.

## 👨‍💻 Author

**Pau Buyreu Real** - Backend Developer
- GitHub: [@paubuyreureal](https://github.com/paubuyreureal)
