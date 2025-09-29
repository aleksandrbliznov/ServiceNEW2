# 🚀 Service PRO - Radicenter Deployment Guide

This guide provides step-by-step instructions for deploying Service PRO to Radicenter hosting with the domain `http://lexanco.eu/servicepro`.

## 📋 System Requirements

- **Python**: 3.6+ (confirmed available on Radicenter)
- **Database**: MySQL (confirmed available on Radicenter)
- **Web Server**: Apache on Linux (confirmed)
- **Domain**: lexanco.eu with subdomain servicepro

## 🛠️ Pre-deployment Setup

### Step 1: Prepare Your Environment

1. **Update your environment variables** in `.env.production`:
   ```bash
   cp .env.production .env
   # Edit .env with your actual database credentials and email settings
   ```

2. **Required environment variables**:
   ```env
   SECRET_KEY=your-super-secret-key-here
   SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost:3306/servicepro_db
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ADMIN_EMAIL=admin@lexanco.eu
   ADMIN_PASSWORD=your-secure-admin-password
   ```

### Step 2: Run Deployment Script

```bash
# Make deployment script executable
chmod +x deploy_radicenter.py

# Run deployment preparation
python deploy_radicenter.py
```

This script will:
- Install Python dependencies
- Set up required directories
- Compile translation files
- Create startup scripts
- Generate .htaccess file

## 📁 File Structure for Upload

Upload these files to your Radicenter hosting (typically `public_html/` or web root):

```
/
├── .env                    # Your environment file
├── .htaccess              # URL routing (created by deploy script)
├── app.py                 # Main Flask application
├── api.py                 # API endpoints
├── requirements.txt       # Python dependencies
├── setup_mysql.py         # Database setup script
├── start.sh               # Startup script (created by deploy script)
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── translations/          # Language files
├── instance/              # Database files (if using SQLite)
└── logs/                  # Application logs
```

## 🗄️ Database Setup

### Step 1: Create MySQL Database

1. **Login to Radicenter control panel**
2. **Create a new MySQL database**:
   - Database name: `servicepro_db`
   - Username: `your_db_user`
   - Password: `your_secure_password`

3. **Update your `.env` file** with the correct database URI:
   ```env
   SQLALCHEMY_DATABASE_URI=mysql://your_db_user:your_secure_password@localhost:3306/servicepro_db
   ```

### Step 2: Initialize Database

```bash
# Run the database setup script
python setup_mysql.py
```

This will create:
- All required tables
- Initial service groups (Kondiiter, Ehitus, Koristus, IT abi)
- Admin user account

## 🌐 Domain Configuration

### Step 1: Main Domain Setup

1. **Point your domain** `lexanco.eu` to your Radicenter hosting
2. **Configure subdomain** `servicepro.lexanco.eu` to point to the same hosting

### Step 2: SSL Certificate (Recommended)

1. **Login to Radicenter control panel**
2. **Navigate to SSL/TLS section**
3. **Generate free Let's Encrypt certificate** for:
   - `lexanco.eu`
   - `servicepro.lexanco.eu`

## 🚀 Starting the Application

### Option 1: Using Startup Script (Recommended)

```bash
# Start the application
./start.sh
```

### Option 2: Manual Start

```bash
# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Start with gunicorn
gunicorn --bind 127.0.0.1:5000 --workers 4 --worker-class sync --log-level info --access-logfile logs/access.log --error-logfile logs/error.log app:app
```

### Option 3: Development Mode (Not recommended for production)

```bash
python app.py
```

## 🔧 Apache Configuration

The deployment script creates a `.htaccess` file that handles:

- **URL routing** to Flask application
- **Security headers** for protection
- **HTTPS redirection** (if SSL is enabled)
- **Static file serving** optimization

### Custom Apache Configuration (Optional)

If you need custom Apache configuration, add this to your `.htaccess` or create a `servicepro.conf` file:

```apache
<VirtualHost *:80>
    ServerName servicepro.lexanco.eu
    DocumentRoot /path/to/your/app

    # Proxy requests to Flask
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    # Security headers
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options SAMEORIGIN
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
```

## 📊 Application URLs

After deployment, your application will be available at:

- **Main site**: `http://lexanco.eu/servicepro`
- **Subdomain**: `http://servicepro.lexanco.eu`
- **Admin panel**: `http://lexanco.eu/servicepro/admin/dashboard`
- **API endpoints**: `http://lexanco.eu/servicepro/api/`

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY in `.env`
- [ ] Use strong passwords for database and admin account
- [ ] Enable SSL certificate
- [ ] Configure firewall rules in Radicenter panel
- [ ] Set up regular database backups
- [ ] Monitor application logs regularly

## 📧 Email Configuration

Configure email settings in your `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
```

**Note**: For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an "App Password"
3. Use the app password (not your regular password)

## 🛠️ Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Test database connection
python -c "from app import db; print('Database connected successfully')"
```

#### Application Not Starting
```bash
# Check Python path and dependencies
python -c "import flask; print('Flask version:', flask.__version__)"
```

#### Permission Errors
```bash
# Fix file permissions
chmod -R 755 .
chmod -R 777 static/uploads logs instance
```

#### Port Already in Use
```bash
# Check what's using port 5000
netstat -tlnp | grep :5000
# Kill process if necessary
kill -9 <PID>
```

### Logs Location

- **Application logs**: `logs/service.log`
- **Access logs**: `logs/access.log`
- **Error logs**: `logs/error.log`

### Getting Help

1. **Check the logs** in the `logs/` directory
2. **Test locally** before deploying
3. **Verify all environment variables** are set correctly
4. **Contact Radicenter support** for hosting-specific issues

## 🔄 Updates and Maintenance

### Updating the Application

1. **Backup your database**:
   ```bash
   mysqldump -u your_db_user -p servicepro_db > backup_$(date +%Y%m%d).sql
   ```

2. **Upload new files** to your hosting

3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restart the application**:
   ```bash
   # Kill existing process
   pkill -f gunicorn
   # Start again
   ./start.sh
   ```

### Regular Maintenance

- **Daily**: Check application logs
- **Weekly**: Review error rates and performance
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Database optimization and cleanup

## 📞 Support

For deployment issues:
1. Check this README file
2. Review the logs in `logs/` directory
3. Test the application locally first
4. Contact development team if needed

---

**Deployment Status**: ✅ Ready for Radicenter hosting
**Last Updated**: 2025
**Python Version**: 3.6+ compatible