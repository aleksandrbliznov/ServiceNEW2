# 🚀 Service PRO - Zone.ee Deployment Guide

**Complete step-by-step guide for deploying Service PRO to zone.ee hosting**

**Application URL:** `https://asbg.ee/servicepro`
**Database:** `d140593_serviceprodb`
**Hosting:** zone.ee

---

## 📋 Prerequisites

- **Domain:** asbg.ee (already configured)
- **Database:** d140593_serviceprodb (already created)
- **SSH Access:** to your zone.ee hosting
- **Python 3.6+:** (available on zone.ee)

---

## 🗂️ Files to Upload

Upload these files to your zone.ee `public_html` directory:

```
public_html/
├── .env                          # Environment configuration
├── .htaccess                     # URL routing
├── app.py                        # Main Flask application
├── api.py                        # API endpoints
├── requirements.txt              # Python dependencies
├── setup_mysql.py                # Database setup script
├── start.sh                      # Startup script
├── static/                       # CSS, JS, images
├── templates/                    # HTML templates
├── translations/                 # Language files
└── instance/                     # Database files (if needed)
```

---

## 🚀 Quick Deployment (5 Steps)

### Step 1: Upload Files via FTP/SFTP
```bash
# Connect to your zone.ee hosting via FTP/SFTP
# Upload all files from your project to public_html/
```

### Step 2: Configure Environment
```bash
# SSH into your zone.ee hosting
ssh your-username@your-server.zone.ee

# Navigate to your project directory
cd public_html

# Copy and edit environment file
cp .env.production .env

# Edit .env with your database password
nano .env
# Update: SQLALCHEMY_DATABASE_URI=mysql://d140593_serviceprodb:YOUR_DB_PASSWORD@localhost:3306/d140593_serviceprodb
```

### Step 3: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install PyMySQL for MySQL support (important!)
pip install PyMySQL
```

### Step 4: Setup Database
```bash
# Run database setup script
python setup_mysql.py

# This will create:
# - All required tables
# - Initial service groups
# - Admin user account
```

### Step 5: Start Application
```bash
# Make startup script executable
chmod +x start.sh

# Start the application
./start.sh

# Or start manually:
gunicorn --bind 127.0.0.1:5000 --workers 4 --worker-class sync --log-level info --access-logfile logs/access.log --error-logfile logs/error.log app:app
```

---

## 🌐 Access Your Application

After deployment, access your application at:
- **Main Site:** `https://asbg.ee/servicepro`
- **Admin Panel:** `https://asbg.ee/servicepro/admin/dashboard`
- **API Endpoints:** `https://asbg.ee/servicepro/api/`

---

## 🔧 Detailed Configuration

### Database Configuration (.env)
```env
# Required: Update with your database password
SQLALCHEMY_DATABASE_URI=mysql://d140593_serviceprodb:YOUR_DB_PASSWORD@localhost:3306/d140593_serviceprodb

# Email Configuration (configure with your SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Security
SECRET_KEY=your-super-secret-key-minimum-32-characters
FLASK_ENV=production

# Domain Configuration
ALLOWED_ORIGINS=https://asbg.ee
```

### URL Routing (.htaccess)
The `.htaccess` file automatically routes:
- `https://asbg.ee/servicepro/` → Flask application
- `https://asbg.ee/servicepro/api/` → API endpoints
- Static files served directly

---

## 🔒 SSL Certificate Setup

### Automatic Setup (Recommended)
```bash
# Install certbot
sudo apt update
sudo apt install certbot python3-certbot-apache

# Generate SSL certificate
sudo certbot --apache -d asbg.ee

# Set up auto-renewal
sudo crontab -e
# Add: 0 3 * * * certbot renew --quiet
```

### Manual SSL Configuration
If certbot is not available, configure SSL manually in your zone.ee control panel:
1. Go to zone.ee control panel
2. Navigate to SSL/TLS section
3. Generate free Let's Encrypt certificate for `asbg.ee`

---

## 🛠️ Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Test database connection
python -c "from app import db; print('Database connected successfully')"

# Check MySQL service status
sudo systemctl status mysql

# Verify database credentials in .env file
cat .env | grep SQLALCHEMY_DATABASE_URI
```

#### Application Not Starting
```bash
# Check Python version
python --version

# Check if port 5000 is available
netstat -tlnp | grep :5000

# Check application logs
tail -f logs/error.log
```

#### Permission Errors
```bash
# Fix file permissions
chmod -R 755 .
chmod -R 777 static/uploads logs instance
```

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
gunicorn --bind 127.0.0.1:8000 ...
```

### Logs Location
- **Application logs:** `logs/service.log`
- **Access logs:** `logs/access.log`
- **Error logs:** `logs/error.log`

---

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Backup database
mysqldump -u d140593_serviceprodb -p d140593_serviceprodb > backup_$(date +%Y%m%d).sql

# Upload new files
# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
pkill -f gunicorn
./start.sh
```

### Regular Maintenance
```bash
# Daily: Check logs
tail -f logs/error.log

# Weekly: Check disk space
df -h

# Monthly: Update packages
pip install -r requirements.txt --upgrade

# Quarterly: Database optimization
mysql -u d140593_serviceprodb -p -e "OPTIMIZE TABLE bookings, services, users;"
```

---

## 📊 Application Features

After deployment, your Service PRO application includes:

### For Customers
- Browse services by category
- Book appointments online
- Leave feedback and ratings
- Multi-language support (ET/EN/RU)

### For Service Providers
- Manage services and pricing
- Set working hours
- View bookings and earnings
- Receive notifications

### For Administrators
- User management
- Service approval system
- Commission tracking
- Analytics dashboard

---

## 📞 Support

### Getting Help
1. Check logs in `logs/` directory
2. Verify all environment variables are set correctly
3. Test database connection
4. Contact zone.ee support for hosting-specific issues

### Emergency Contacts
- **Zone.ee Support:** https://zone.ee/support
- **Development Team:** For application-specific issues

---

## ✅ Deployment Checklist

- [ ] Files uploaded to public_html
- [ ] .env file configured with database password
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Database setup completed (python setup_mysql.py)
- [ ] Application started (./start.sh)
- [ ] SSL certificate configured
- [ ] Domain pointing to hosting
- [ ] Application accessible at https://asbg.ee/servicepro

---

**🎉 Deployment Status:** ✅ Ready for zone.ee hosting
**📅 Last Updated:** 2025-09-29
**🏠 Hosting:** zone.ee