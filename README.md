# Service PRO

A complete service booking application built with Python Flask, featuring user registration, admin panel, handyman management, and modern design.

## Features

### 🔐 User Management
- **User Registration**: Customers can register with the system
- **Role-based Access**: Three user roles - Customer, Admin, Handyman
- **Secure Authentication**: Password hashing and session management
- **Profile Management**: Users can manage their profiles

### 🛠️ Service Management
- **Service Catalog**: Admins can manage available services
- **Service Booking**: Customers can book services online
- **Booking Management**: Track booking status and history
- **Special Requests**: Customers can add special requirements

### 👨‍🔧 Handyman System
- **Handyman Registration**: Professionals can register as service providers
- **Admin Approval**: All handyman registrations require admin approval
- **Job Assignment**: Admins assign jobs to approved handymen
- **Status Tracking**: Handymen can update job progress

### 🎛️ Admin Panel
- **User Management**: Approve/reject handyman registrations
- **Booking Oversight**: Manage all bookings and assignments
- **System Statistics**: View platform usage statistics
- **Complete Control**: Full administrative access

### 🎨 Modern Design
- **Responsive UI**: Works on desktop and mobile devices
- **Bootstrap 5**: Modern, clean interface
- **Interactive Elements**: Smooth animations and transitions
- **User-friendly**: Intuitive navigation and workflows
- **Modern Landing Page**: Professional landing page with hero section, service cards, features, and contact form
- **Glass Morphism Effects**: Modern card designs with backdrop blur effects
- **CSS Variables**: Consistent theming with CSS custom properties

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL/MySQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Icons**: Font Awesome
- **Email**: Flask-Mail with SMTP

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd service-app
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env` file and update with your settings:
   ```bash
   cp .env .env.local  # Create a copy
   # Edit .env.local with your email credentials and database settings
   ```

5. **Setup database** (choose one option):

   **Option A: SQLite (default, but may have Windows compatibility issues)**
   ```bash
   python create_working_db.py
   ```

   **Option B: PostgreSQL (recommended for production)**
   ```bash
   # Install PostgreSQL and create database first
   # Update .env with PostgreSQL connection string
   SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/service_pro
   # Then run:
   python setup_postgresql.py
   ```

   **Option C: MySQL (alternative option)**
   ```bash
   # Install MySQL and create database first
   # Update .env with MySQL connection string
   SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost:3306/service_pro
   # Then run:
   python setup_postgresql.py
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser**:
   Navigate to `http://localhost:5000`

## Default Login Credentials

The application comes with pre-configured test accounts for immediate use:

| Role | Username | Password | Status |
|------|----------|----------|--------|
| 👑 **Admin** | `admin` | `admin123` | ✅ Active |
| 👤 **Customer** | `customer` | `customer123` | ✅ Active |
| 🔧 **Service Provider** | `handyman` | `handyman123` | ✅ Active |

## Sample Services Available

The application includes 6 sample services ready for booking:

| Service | Category | Price | Duration |
|---------|----------|-------|----------|
| Plumbing Repair | Plumbing | $75 | 2 hours |
| Electrical Installation | Electrical | $85 | 3 hours |
| House Cleaning | Cleaning | $120 | 4 hours |
| Garden Maintenance | Gardening | $60 | 2 hours |
| Painting Services | Painting | $200 | 6 hours |
| Carpentry Work | Carpentry | $90 | 4 hours |

## Project Structure

```
service-app/
├── app.py                 # Main Flask application
├── setup.py              # Database initialization script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── user_dashboard.html    # Customer dashboard
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── handyman_dashboard.html # Handyman dashboard
│   ├── admin_users.html       # User management
│   ├── admin_bookings.html    # Booking management
│   ├── assign_handyman.html   # Assign handyman to booking
│   └── book_service.html      # Service booking form
└── static/             # Static assets
    ├── css/
    │   ├── style.css        # Main custom styles
    │   └── site-modern.css  # Modern landing page styles
    └── js/
        └── script.js   # JavaScript functionality
```

## Database Configuration

The application supports multiple database backends:

### SQLite (Default)
```bash
# In .env file
SQLALCHEMY_DATABASE_URI=sqlite:///service_app.db
```

**Note**: SQLite may have compatibility issues on some Windows systems. If you encounter database connection errors, use PostgreSQL instead.

### PostgreSQL (Recommended)
```bash
# Install PostgreSQL and create database first
createdb service_pro

# In .env file
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/service_pro
```

### MySQL (Alternative)
```bash
# Install MySQL and create database first
mysql -u root -p
CREATE DATABASE service_pro;

# In .env file
SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost:3306/service_pro
```

## Database Models

### User
- **id**: Primary key
- **username**: Unique username
- **email**: User email address
- **password_hash**: Hashed password
- **role**: User role (admin, user, handyman)
- **first_name**, **last_name**: User's name
- **phone**: Contact phone number
- **address**: User address
- **is_approved**: Approval status for handymen
- **created_at**: Registration timestamp

### Service
- **id**: Primary key
- **name**: Service name
- **description**: Service description
- **price**: Service cost
- **duration_hours**: Estimated duration
- **category**: Service category
- **is_active**: Whether service is available
- **created_at**: Creation timestamp

### Booking
- **id**: Primary key
- **user_id**: Customer who made the booking
- **service_id**: Booked service
- **handyman_id**: Assigned handyman (optional)
- **booking_date**: Scheduled date and time
- **status**: Booking status (pending, approved, in_progress, completed, cancelled)
- **special_requests**: Customer requirements
- **total_price**: Final price
- **created_at**: Booking creation timestamp

## Workflow

1. **Customer Registration**: Users register as customers
2. **Handyman Registration**: Professionals register and wait for admin approval
3. **Service Booking**: Customers browse and book available services
4. **Admin Review**: Admins review new handyman registrations
5. **Booking Approval**: Admins review and approve customer bookings
6. **Handyman Assignment**: Admins assign approved bookings to handymen
7. **Job Execution**: Handymen complete assigned jobs and update status
8. **Completion**: Jobs are marked complete and customers are notified

## API Endpoints

The application provides a web interface for all operations. Key routes include:

- `/` - Home page with service catalog
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/user/dashboard` - Customer dashboard
- `/admin/dashboard` - Admin dashboard
- `/handyman/dashboard` - Handyman dashboard
- `/admin/users` - User management
- `/admin/bookings` - Booking management

## Development

### Adding New Services
Admins can add new services through the admin panel (functionality can be extended).

### Customizing Design
Modify `static/css/style.css` to customize the appearance.

### Adding Features
The modular Flask structure makes it easy to add new features and routes.

## Security Features

- **Password Hashing**: All passwords are securely hashed
- **Session Management**: Secure user sessions with Flask-Login
- **Role-based Access**: Different permissions for different user types
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Built-in CSRF protection with Flask-WTF
- **Environment Variables**: Sensitive configuration stored securely
- **Email Security**: App passwords for Gmail integration

## Recent Fixes and Improvements

### ✅ Database Schema Updates
- Added missing `reset_token` and `reset_token_expiry` columns to User model
- Added `admin_approved` field to User and Booking models
- Improved database migration handling

### 🔧 Configuration Improvements
- Moved all configuration to environment variables
- Created `.env` file template for secure credential storage
- Removed hard-coded credentials from source code

### 🐛 Bug Fixes
- Fixed admin login test to work with Estonian interface
- Corrected booking status inconsistency (pending vs confirmed)
- Updated email notifications to match booking status
- Improved error handling throughout the application

### 📧 Email Configuration
- Secure email configuration using environment variables
- Support for Gmail app passwords
- Better error handling for email failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ using Python Flask**