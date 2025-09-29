# Password Manager

Aplicación web segura para gestionar contraseñas y credenciales, construida con Django REST Framework en el backend y React en el frontend, completamente containerizada con Docker y desplegada en GitHub Codespaces.

## 🚀 Demo

**Accede a la aplicación directamente:** [Abrir en GitHub Codespaces](https://github.com/paubuyreureal/PasswordManager)

La aplicación está completamente funcional y lista para probar con:
- Registro y autenticación de usuarios
- Almacenamiento seguro de contraseñas con cifrado
- Funcionalidad de recuperación de contraseña (e-mail en consola)
- Capacidades de búsqueda y filtrado

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.9** con **Django 4.2** y **Django REST Framework**
- **PostgreSQL** como base de datos principal
- **Autenticación JWT** con tokens de actualización
- **Cifrado AES** para contraseñas almacenadas
- **bcrypt** para hash de contraseñas de usuario

### Frontend
- **React 18** con **Vite** como herramienta de build
- **Tailwind CSS** para estilos
- **React Router** para navegación
- **Axios** para comunicación con la API

### Infraestructura
- **Docker** y **Docker Compose** para containerización
- **GitHub Codespaces** para despliegue en la nube
- **Nginx** como proxy inverso y servidor de archivos estáticos
- **DevContainer** configurado para desarrollo sin fricciones

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│────│  Nginx Proxy    │────│ Django Backend  │
│   (Puerto 3000) │    │   (Puerto 80)   │    │   (Puerto 8000) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                               ┌─────────────────┐
                                               │   PostgreSQL    │
                                               │   (Puerto 5432) │
                                               └─────────────────┘
```

## 🚀 Inicio Rápido

### GitHub Codespaces

1. **Haz clic en el botón "Code"** en este repositorio
2. **Selecciona "Codespaces"** → **"Create codespace on main"**
3. **Espera varios minutos** para la configuración automática (se instalan automáticamente las dependencias)
4. **Accede a la aplicación** en el puerto reenviado (normalmente puerto 3000)

## 📋 Variables de Entorno

La aplicación utiliza el archivo `codespaces.env` para la configuración en Codespaces. Para referencia, consulta `docker.env.example` que contiene la plantilla de todas las variables necesarias:

- **Configuración de email** (para recuperación de contraseña) --- NO USADO EN VERSIÓN ACTUAL
- **Configuración de Django** (SECRET_KEY, DEBUG, etc.)
- **Base de datos** (configurada automáticamente en Docker)

## 🔌 Endpoints de la API (Probar a través del Frontend)

### Autenticación
```bash
# Registro de usuario
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

# Solicitud de recuperación de contraseña
POST /api/password-reset/
{
  "username": "testuser"
}

# Confirmación de recuperación de contraseña
POST /api/password-reset/confirm/
{
  "token": "reset-token",
  "password": "newpassword"
}
```

### Gestión de Contraseñas (Requiere Autenticación)
```bash
# Obtener todas las cuentas
GET /api/accounts/

# Crear nueva cuenta
POST /api/accounts/
{
  "username": "gmail_user",
  "password": "gmail_password",
  "url": "https://gmail.com",
  "notes": "Cuenta de email personal"
}

# Actualizar cuenta
PUT /api/accounts/{id}/
{
  "username": "updated_user",
  "password": "new_password",
  "url": "https://updated-site.com"
}

# Eliminar cuenta
DELETE /api/accounts/{id}/

# Buscar cuentas
GET /api/accounts/?search=gmail
GET /api/accounts/?url_filter=google.com
```

## 🔄 Funcionalidad de Recuperación de Contraseña

**Importante:** En la versión actual, no se envía un correo electrónico real. En su lugar, el contenido del correo se imprime en los logs del backend donde se puede acceder al enlace para restablecer la contraseña. Para esta función, acceder a los logs a través de Codespaces.

### Cómo funciona:

1. **Usuario solicita recuperación:** Introduce su nombre de usuario
2. **Backend genera enlace:** Se crea un token seguro y se genera el enlace
3. **Email se imprime en logs:** El contenido completo del email aparece en los logs del backend
4. **Acceso a logs:** Para ver el email y el enlace:
   ```bash
   docker compose -f docker-compose.codespaces.yml logs -f backend
   ```
   o en la sección de **Containers**, botón derecho sobre el container del Backend y seleccionar **View Logs**
5. **Uso del enlace:** Copia el enlace de los logs y ábrelo en el navegador para restablecer la contraseña

Esta implementación permite probar la funcionalidad completa sin necesidad de configurar un servidor de email real.

## 👨‍💻 Autor

**Pau Buyreu Real** - Desarrollador Backend
- GitHub: [@paubuyreureal](https://github.com/paubuyreureal)
