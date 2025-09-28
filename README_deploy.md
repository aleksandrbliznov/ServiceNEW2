# 🚀 Deployment Guide - Service PRO

This guide provides comprehensive instructions for deploying the Service PRO application to various web hosting platforms. The application consists of a Python Flask backend and a Next.js frontend.

## 📋 Deployment Options

Choose from the following deployment platforms based on your needs:

### 🟢 Recommended for Beginners
- **Heroku** - Simple deployment with free tier
- **Railway** - Modern alternative to Heroku
- **Render** - Free tier with generous limits

### 🟡 Recommended for Production
- **DigitalOcean App Platform** - Scalable and cost-effective
- **AWS (EC2 + RDS)** - Full control and scalability
- **Google Cloud Run** - Serverless deployment

### 🔵 Enterprise Options
- **AWS Elastic Beanstalk** - Managed platform
- **Google App Engine** - Platform as a Service
- **Azure App Service** - Microsoft cloud platform

## 🏗️ Deployment Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Next.js       │    │   Flask API      │
│   Frontend      │◄──►│   Backend        │
│   (Port 3000)   │    │   (Port 5000)    │
└─────────────────┘    └──────────────────┘
         │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │   Database       │
                    │   (Port 5432)    │
                    └──────────────────┘
```

## 🚀 Quick Start Deployment

### Option 1: Heroku (Easiest)

#### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [Git](https://git-scm.com/)

#### Step 1: Prepare Your Application
```bash
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon (recommended)
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

#### Step 2: Configure for Heroku
Create a `Procfile` in your root directory:
```
web: cd frontend && npm run build && npm run start & cd .. && gunicorn --worker-tmp-dir /dev/shm app:app
```

Create a `runtime.txt`:
```
python-3.11.5
```

#### Step 3: Deploy
```bash
# Add files and commit
git add .
git commit -m "Prepare for deployment"

# Deploy to Heroku
git push heroku main
```

#### Step 4: Run Database Migrations
```bash
heroku run python setup_postgresql.py
```

### Option 2: Railway (Modern Alternative)

#### Step 1: Connect Repository
1. Connect your GitHub repository to [Railway](https://railway.app)
2. Railway will auto-detect it's a Python project

#### Step 2: Add PostgreSQL Database
```bash
# Railway CLI
railway add postgresql
```

#### Step 3: Set Environment Variables
Add these variables in Railway dashboard:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=${{PostgreSQL.RAILWAY_STATIC_URL}}
```

#### Step 4: Deploy
Railway will automatically deploy on push to main branch.

## ⚙️ Detailed Configuration

### Environment Variables

Create a `.env` file with production values:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-64-characters-long
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:5432/database_name
FLASK_ENV=production

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application Settings
UPLOAD_FOLDER=static/uploads
BABEL_DEFAULT_LOCALE=et
BABEL_SUPPORTED_LOCALES=et,en,ru

# Security Settings (Production)
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict
PERMANENT_SESSION_LIFETIME=3600

# Production Optimizations
FLASK_DEBUG=False
```

### Database Configuration

#### PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE service_pro;

-- Create user
CREATE USER service_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE service_pro TO service_user;

-- Connect and run migrations
psql -h localhost -U service_user -d service_pro
```

Then run:
```bash
python setup_postgresql.py
```

#### MySQL Alternative
```sql
CREATE DATABASE service_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'service_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON service_pro.* TO 'service_user'@'localhost';
FLUSH PRIVILEGES;
```

### Frontend Build Configuration

#### Next.js Production Build
```bash
cd frontend
npm install
npm run build
npm run start
```

#### Static Export (Optional)
For static hosting, modify `next.config.ts`:
```typescript
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}
```

## 🌐 Domain & SSL Configuration

### Custom Domain Setup

#### Heroku
```bash
# Add custom domain
heroku domains:add www.yourdomain.com

# Generate SSL certificate (automatic with paid dynos)
heroku certs:auto:enable
```

#### Railway
1. Go to Railway dashboard
2. Navigate to your service settings
3. Add custom domain in "Domains" section

### SSL Certificate

#### Let's Encrypt (Free)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### Cloudflare (Recommended)
1. Add your domain to Cloudflare
2. Enable SSL/TLS encryption
3. Set encryption mode to "Full (strict)"

## 📊 Production Optimizations

### Performance Tuning

#### Flask Configuration
```python
# In app.py - Production settings
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Monitoring & Logging

#### Application Monitoring
```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/service.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Service startup')
```

#### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

## 🔧 Platform-Specific Guides

### DigitalOcean App Platform

1. **Create App**:
   - Go to DigitalOcean Cloud Panel
   - Create new app from GitHub
   - Select Python environment

2. **Configure Build**:
   ```yaml
   # digitalocean-app.yaml
   name: service-pro
   services:
     - name: web
       github:
         repo: your-repo/service-pro
         branch: main
       build_command: pip install -r requirements.txt && cd frontend && npm install && npm run build
       run_command: cd frontend && npm start
       environment_slug: python
       envs:
         - key: FLASK_ENV
           value: production
   ```

### AWS Deployment

#### Using Elastic Beanstalk

1. **Create Application**:
   ```bash
   # Install EB CLI
   pip install awsebcli

   # Initialize application
   eb init service-pro --platform python-3.11 --region us-east-1

   # Create environment
   eb create production-env
   ```

2. **Configure Database**:
   - Create RDS PostgreSQL instance
   - Update environment variables
   - Deploy with `eb deploy`

### Google Cloud Run

1. **Build Container**:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   RUN cd frontend && npm install && npm run build

   EXPOSE 5000
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

2. **Deploy**:
   ```bash
   gcloud run deploy --source . --platform managed --region us-central1
   ```

## 🛠️ Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database connectivity
python -c "from app import db; db.create_all()"

# Verify environment variables
heroku config | grep DATABASE
```

#### Build Failures
```bash
# Check build logs
heroku logs --tail

# Debug locally
FLASK_ENV=production python app.py
```

#### Static Files Not Loading
- Ensure `static/` directory is accessible
- Check file permissions
- Verify Nginx configuration

### Performance Issues

#### Memory Optimization
```python
# Add to app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

#### Database Query Optimization
```python
# Use connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True
}
```

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Configure security headers
- [ ] Set up database backups
- [ ] Enable firewall rules
- [ ] Use strong passwords
- [ ] Regular dependency updates
- [ ] Monitor for vulnerabilities

## 📞 Support & Maintenance

### Regular Tasks
1. **Daily**: Check application logs
2. **Weekly**: Review error rates and performance
3. **Monthly**: Update dependencies and security patches
4. **Quarterly**: Database optimization and cleanup

### Backup Strategy
```bash
# Database backup
pg_dump service_pro > backup_$(date +%Y%m%d).sql

# File backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz --exclude='*.log' --exclude='__pycache__' .
```

### Monitoring Tools
- **Uptime**: UptimeRobot, Pingdom
- **Performance**: New Relic, DataDog
- **Logs**: Papertrail, Logentries
- **Errors**: Sentry, Rollbar

## 📚 Additional Resources

- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Next.js Production Checklist](https://nextjs.org/docs/advanced-features/security-headers)
- [PostgreSQL Production Setup](https://wiki.postgresql.org/wiki/Production_Database_Setup)
- [Nginx Configuration Guide](https://docs.nginx.com/nginx/admin-guide/web-server/)

---

**Need help?** Create an issue in the repository or contact the development team.