# 🚀 GitHub Codespaces Setup

This Password Manager application is configured to run seamlessly in GitHub Codespaces for technical demonstrations and code reviews.

## 🏗️ Architecture

- **Frontend**: React app served by Nginx (Port 3000)
- **Backend**: Django REST API (Port 8000)
- **Database**: PostgreSQL (Port 5432)
- **Email**: Console backend (logs to terminal)

## 📦 What's Included

### Docker Configuration
- `docker-compose.codespaces.yml` - Optimized for Codespaces
- `codespaces.env` - Safe environment variables for demos
- `.devcontainer/devcontainer.json` - Automatic setup

### Key Features
- ✅ **Automatic Setup**: Everything starts automatically when Codespace opens
- ✅ **Console Email**: Password reset emails print to terminal logs
- ✅ **PostgreSQL**: Automatically creates database and runs migrations
- ✅ **Hot Reload**: Code changes reflect immediately
- ✅ **Port Forwarding**: All services accessible via Codespaces URLs

## 🚀 Quick Start

1. **Open in Codespaces**: Click "Code" → "Codespaces" → "Create codespace"
2. **Wait for Setup**: The devcontainer will automatically build and start
3. **Access Application**:
   - Frontend: Port 3000 (will be auto-forwarded)
   - Backend API: Port 8000
   - Database: Port 5432

## 📧 Password Reset Testing

When testing password reset functionality:
1. Go to "Forgot Password" in the frontend
2. Enter any email address
3. Check the terminal logs in Codespaces - you'll see the reset email content
4. Use the reset link from the logs to test the flow

## 🔧 Development Commands

```bash
# View all logs
docker-compose -f docker-compose.codespaces.yml logs -f

# Restart services
docker-compose -f docker-compose.codespaces.yml restart

# Access database
docker-compose -f docker-compose.codespaces.yml exec db psql -U postgres -d passwordmanager

# Run Django commands
docker-compose -f docker-compose.codespaces.yml exec backend python manage.py createsuperuser
docker-compose -f docker-compose.codespaces.yml exec backend python manage.py shell

# Stop everything
docker-compose -f docker-compose.codespaces.yml down
```

## 🎯 Testing the Application

### 1. Create Account
- Register a new user account
- Login with credentials

### 2. Add Password Entries
- Create accounts for various services (GitHub, Google, etc.)
- Test password encryption/decryption
- Try the favicon fetching feature

### 3. Test Password Reset
- Use "Forgot Password" feature
- Check terminal for email content
- Complete password reset flow

### 4. Explore Features
- Search and filter accounts
- Edit/delete entries
- Test responsive design

## 🔍 Code Review Focus Areas

### Backend (Django)
- **Models**: `backend/api/models.py` - Account model with encryption
- **Views**: `backend/api/views.py` - REST API endpoints
- **Serializers**: `backend/api/serializers.py` - Data validation
- **Security**: Password encryption, JWT authentication

### Frontend (React)
- **Components**: `frontend/src/components/` - Reusable UI components
- **Pages**: `frontend/src/pages/` - Main application screens
- **API**: `frontend/src/api.js` - Backend communication
- **Styling**: CSS modules for component styling

### Docker Configuration
- **Multi-stage builds** for optimized images
- **Health checks** for reliable startup
- **Volume mounts** for development
- **Environment configuration** for different deployments

## 🛠️ Troubleshooting

### Services Not Starting
```bash
# Check service status
docker-compose -f docker-compose.codespaces.yml ps

# View specific service logs
docker-compose -f docker-compose.codespaces.yml logs backend
```

### Database Issues
```bash
# Reset database
docker-compose -f docker-compose.codespaces.yml down -v
docker-compose -f docker-compose.codespaces.yml up --build
```

### Port Issues
- Codespaces automatically forwards ports 3000 and 8000
- Check the "Ports" tab in VS Code for forwarded URLs

## 📝 Notes

- All sensitive data uses demo keys (safe for technical tests)
- Email functionality uses console backend (no real emails sent)
- Database persists between Codespace restarts
- Perfect for code reviews and technical demonstrations!
