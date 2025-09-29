# 🚂 Service PRO - Railway Deployment Guide

**Complete step-by-step guide for deploying Service PRO to Railway**

**Platform:** Railway.app
**Database:** PostgreSQL (auto-provisioned)
**Runtime:** Python 3.11+
**Deployment:** Git-based with automatic deployments

---

## 📋 Prerequisites

- **Railway Account:** https://railway.app (free tier available)
- **Git Repository:** Your project pushed to GitHub/GitLab
- **Python 3.6+:** (Railway supports Python 3.11+)

---

## 🚀 Quick Deployment (3 Steps)

### Step 1: Connect to Railway
```bash
# Install Railway CLI (optional, can use web dashboard)
npm install -g @railway/cli
railway login

# Or use Railway web dashboard at https://railway.app
```

### Step 2: Create New Project
```bash
# Create new Railway project
railway init

# Select: "Empty Project"
# Name: "service-pro" (or your preferred name)
```

### Step 3: Deploy Application
```bash
# Add PostgreSQL database (Railway does this automatically)
railway add postgresql

# Connect your Git repository
railway connect

# Deploy (Railway will automatically detect Python/Flask)
railway up

# Your app will be available at: https://your-app.railway.app
```

---

## ⚙️ Railway Dashboard Configuration

### 1. Environment Variables
After deployment, go to your Railway project dashboard and add these variables:

**Required Variables:**
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-minimum-32-characters
```

**Optional Variables:**
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
BABEL_DEFAULT_LOCALE=et
```

**Railway Auto-populated Variables (don't change):**
- `DATABASE_URL` - PostgreSQL connection string
- `RAILWAY_STATIC_URL` - Your app's domain
- `PORT` - Port for your application

### 2. Database Setup
Railway automatically:
- ✅ Creates PostgreSQL database
- ✅ Sets up `DATABASE_URL` environment variable
- ✅ Handles database migrations
- ✅ Provides database backups

### 3. Domain Configuration (Optional)
For custom domain:
```bash
# Add custom domain in Railway dashboard
railway domain add yourdomain.com

# Railway will automatically:
# - Generate SSL certificate
# - Configure DNS settings
# - Set up HTTPS redirect
```

---

## 🔧 Manual Deployment (Alternative)

### Using Railway CLI
```bash
# Login to Railway
railway login

# Create new project
railway init --name service-pro

# Add PostgreSQL
railway add postgresql

# Connect Git repository
railway connect

# Set environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key

# Deploy
railway up
```

### Using GitHub Integration
1. **Connect GitHub:** Link your repository to Railway
2. **Auto-deploy:** Enable automatic deployments on push
3. **Branch protection:** Set deployment branch (main/master)

---

## 📁 Project Structure for Railway

Your project should include these files:

**Important:** The `main.py` file is required for Railway deployment. It serves as the WSGI entry point that Railway's gunicorn server uses to run your application.

```
/
├── main.py               # Railway WSGI entry point (required for Railway)
├── app.py                 # Main Flask application
├── api.py                 # API endpoints
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local development)
├── .env.production       # Production environment template
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── translations/         # Language files
└── railway.toml          # Railway configuration (optional)
```

### Railway Configuration (Optional)
Create `railway.toml` for custom settings:

```toml
[build]
builder = "python"

[deploy]
startCommand = "gunicorn --bind 0.0.0.0:$PORT --workers 4 main:application"

[[services]]
name = "service-pro"
```

---

## 🔒 Security & SSL

Railway automatically provides:
- ✅ **Free SSL certificates** (Let's Encrypt)
- ✅ **HTTPS redirection** (automatic)
- ✅ **Security headers** (configurable)
- ✅ **DDoS protection** (built-in)

### Custom Security Headers
Add to your Flask application:
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## 🗄️ Database Management

### Automatic Setup
Railway automatically:
- Creates PostgreSQL database
- Sets up user and permissions
- Provides connection string via `DATABASE_URL`
- Handles backups and scaling

### Database Operations
```bash
# Connect to database via Railway CLI
railway connect postgresql

# Or use Railway dashboard to access database

# Manual connection (if needed)
psql $DATABASE_URL
```

### Database Schema
Railway will automatically create tables when you run:
```bash
# First deployment - tables created automatically
python -c "from app import db; db.create_all()"
```

---

## 🚨 Monitoring & Logs

### Accessing Logs
```bash
# View application logs
railway logs

# View specific service logs
railway logs --service service-pro

# Stream logs in real-time
railway logs --follow
```

### Railway Dashboard Monitoring
- **Real-time metrics** (CPU, Memory, Network)
- **Error tracking** and alerts
- **Performance graphs**
- **Database monitoring**

---

## 🔧 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check build logs
railway logs --build

# Common fixes:
# 1. Ensure requirements.txt is correct
# 2. Check Python version compatibility
# 3. Verify all dependencies are included
# 4. Make sure main.py exists for Railway WSGI entry point
```

#### ModuleNotFoundError: No module named 'main'
```bash
# This error occurs when Railway can't find the WSGI entry point
# Solution: Ensure main.py file exists in your project root
# The main.py file should contain:
# application = app  # Your Flask app instance
# Railway expects this structure for gunicorn deployment
```

#### ModuleNotFoundError: No module named 'flask_sqlalchemy'
```bash
# This error occurs when Flask-SQLAlchemy is not installed
# Solution: Add Flask-SQLAlchemy to requirements.txt
# Make sure requirements.txt includes: Flask-SQLAlchemy==3.0.5
# Railway will automatically install dependencies on deployment
```

#### Database Connection Issues
```bash
# Test database connection
railway run python -c "from app import db; print('Database connected')"

# Check DATABASE_URL variable
railway variables get DATABASE_URL
```

#### Port Binding Issues
```bash
# Railway automatically sets PORT variable
# Make sure your app uses: app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
```

#### Static Files Not Serving
```bash
# Ensure static folder exists and contains files
railway run ls -la static/

# Check Flask static configuration
railway run python -c "from app import app; print(app.static_folder)"
```

### Debug Mode
```bash
# Enable debug logging
railway variables set FLASK_DEBUG=True

# View detailed logs
railway logs --tail 100
```

---

## 🚀 Scaling & Performance

### Automatic Scaling
Railway automatically scales based on:
- CPU usage
- Memory consumption
- Network traffic

### Manual Scaling
```bash
# Check current resource usage
railway status

# Upgrade plan for more resources (if needed)
# Railway dashboard → Settings → Plan
```

### Performance Optimization
```bash
# Use gunicorn for production
pip install gunicorn

# Configure worker processes
railway variables set WEB_CONCURRENCY=4
```

---

## 🔄 Updates and Maintenance

### Automatic Deployments
```bash
# Push to connected Git repository
git add .
git commit -m "Update application"
git push

# Railway automatically redeploys
```

### Manual Redeployment
```bash
# Force redeployment
railway up --force

# Rollback to previous version
railway rollback
```

### Database Migrations
```bash
# Run database migrations
railway run python -c "from app import db; db.create_all()"

# Backup database
railway run pg_dump $DATABASE_URL > backup.sql
```

---

## 📊 Application URLs

After deployment, your application will be available at:
- **Main Site:** `https://your-app.railway.app`
- **Admin Panel:** `https://your-app.railway.app/admin/dashboard`
- **API Endpoints:** `https://your-app.railway.app/api/`

---

## 🛠️ Development Workflow

### Local Development
```bash
# Set up local environment
cp .env.production .env
# Edit .env with local database settings

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

### Production Deployment
```bash
# Deploy to Railway
railway up

# Check deployment status
railway status

# View logs
railway logs --follow
```

---

## 📞 Support & Resources

### Railway Documentation
- **Official Docs:** https://docs.railway.app
- **Python Guide:** https://docs.railway.app/deploy/python
- **PostgreSQL:** https://docs.railway.app/database/postgresql

### Getting Help
1. **Railway Discord:** https://discord.gg/railway
2. **Railway Status:** https://status.railway.app
3. **Check logs:** `railway logs --follow`

### Emergency Contacts
- **Railway Support:** Use in-app chat or Discord
- **Development Team:** For application-specific issues

---

## ✅ Deployment Checklist

- [ ] Railway account created and verified
- [ ] Git repository connected to Railway
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] Application successfully deployed
- [ ] Database tables created
- [ ] Application accessible at railway.app domain
- [ ] SSL certificate active
- [ ] Logs accessible and error-free

---

## 🎯 Advanced Features

### Custom Domain
```bash
# Add custom domain
railway domain add yourdomain.com

# Configure DNS (Railway provides settings)
# - CNAME record to railway.app
# - SSL certificate auto-generated
```

### Multiple Environments
```bash
# Create staging environment
railway environment create staging

# Deploy to specific environment
railway up --environment staging
```

### Database Backups
```bash
# Manual backup
railway run pg_dump $DATABASE_URL > backup.sql

# Railway automatic backups (daily)
# Access via Railway dashboard
```

---

**🚂 Deployment Status:** ✅ Ready for Railway hosting
**📅 Last Updated:** 2025-09-29
**🏆 Platform:** Railway.app
**💾 Database:** PostgreSQL (auto-provisioned)