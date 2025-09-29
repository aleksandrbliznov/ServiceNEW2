# 🔒 SSL Setup Guide for Radicenter

## Automatic SSL with Let's Encrypt (Free)

### Step 1: Install Certbot
```bash
# Install snap (if not already installed)
sudo apt update
sudo apt install snapd

# Install certbot
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

# Create symlink
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### Step 2: Generate SSL Certificate
```bash
# Stop your application temporarily
sudo systemctl stop apache2  # or your web server

# Generate certificate for both domains
sudo certbot certonly --standalone \
  -d lexanco.eu \
  -d servicepro.lexanco.eu \
  --agree-tos \
  --register-unsafely-without-email \
  --no-eff-email

# Start your application again
sudo systemctl start apache2  # or your web server
```

### Step 3: Configure Auto-renewal
```bash
# Test renewal (dry run)
sudo certbot renew --dry-run

# Enable auto-renewal (runs twice daily)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Manual SSL Configuration

### Update .htaccess for HTTPS
```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Security headers for HTTPS
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
```

### Update Flask Configuration
In your `.env` file:
```env
# Enable HTTPS in production
SESSION_COOKIE_SECURE=True
REMEMBER_COOKIE_SECURE=True
```

## SSL Certificate Locations

After generation, certificates are typically located at:
- **Certificate**: `/etc/letsencrypt/live/lexanco.eu/cert.pem`
- **Private Key**: `/etc/letsencrypt/live/lexanco.eu/privkey.pem`
- **Chain File**: `/etc/letsencrypt/live/lexanco.eu/chain.pem`

## Verification

### Test SSL Installation
```bash
# Test with curl
curl -I https://lexanco.eu
curl -I https://servicepro.lexanco.eu

# Test with SSL Labs
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=lexanco.eu
```

### Check Certificate Details
```bash
# View certificate info
openssl x509 -in /etc/letsencrypt/live/lexanco.eu/cert.pem -text -noout

# Check expiration date
openssl x509 -in /etc/letsencrypt/live/lexanco.eu/cert.pem -enddate -noout
```

## Troubleshooting SSL

### Common Issues

#### Certificate Not Found
```bash
# Check if certificate exists
sudo ls -la /etc/letsencrypt/live/lexanco.eu/

# Reissue certificate if needed
sudo certbot certonly --standalone -d lexanco.eu -d servicepro.lexanco.eu --force-renewal
```

#### Mixed Content Warnings
- Ensure all resources (CSS, JS, images) use HTTPS URLs
- Update your Flask app to serve static files with HTTPS
- Check for hardcoded HTTP URLs in templates

#### Port 80 Blocked
```bash
# Check if port 80 is open
sudo netstat -tlnp | grep :80

# Allow HTTP traffic in firewall
sudo ufw allow 80
sudo ufw allow 443
```

## Security Best Practices

- [ ] Use strong SSL protocols (TLS 1.2+)
- [ ] Enable HSTS headers
- [ ] Set up certificate auto-renewal
- [ ] Monitor certificate expiration
- [ ] Use secure cipher suites
- [ ] Enable OCSP stapling

## Monitoring SSL Certificates

### Check Expiration
```bash
# Manual check
sudo certbot certificates

# Automated monitoring script
#!/bin/bash
EXPIRY=$(openssl x509 -in /etc/letsencrypt/live/lexanco.eu/cert.pem -enddate -noout | cut -d= -f2)
echo "Certificate expires: $EXPIRY"
```

### Auto-renewal Logs
```bash
# Check renewal logs
sudo systemctl status certbot.timer
sudo journalctl -u certbot.timer --no-pager
```

---

**SSL Status**: ✅ Ready for setup
**Recommended**: Let's Encrypt (Free and automatic)