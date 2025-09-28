# Service PRO

A complete service booking application built with Python Flask, featuring user registration, admin panel, handyman management, modern responsive design, and multi-language support.

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

### 🌍 Internationalization (i18n)
- **Multi-language Support**: Estonian (et) and Russian (ru) languages
- **Flask-Babel Integration**: Complete translation system
- **Dynamic Language Switching**: Users can switch languages
- **Translated Content**: All UI text and messages translated

### 🎨 Modern Design & UX
- **Fully Responsive UI**: Optimized for desktop, tablet, and mobile devices
- **Bootstrap 5**: Modern, clean interface with enhanced components
- **Interactive Elements**: Smooth animations, hover effects, and micro-interactions
- **User-friendly**: Intuitive navigation and streamlined workflows
- **Modern Landing Page**: Professional hero section, service cards, features showcase, and contact form
- **Glass Morphism Effects**: Modern card designs with backdrop blur effects
- **CSS Variables**: Consistent theming with ServiceNEW2 brand colors
- **Enhanced Accessibility**: WCAG compliant with screen reader support, keyboard navigation, and high contrast mode
- **Loading States**: Visual feedback for all user actions
- **Touch-friendly**: Optimized touch targets for mobile devices

## Technology Stack

- **Backend**: Python Flask with enhanced security and error handling
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL/MySQL support
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript with modern animations
- **Authentication**: Flask-Login with secure session management
- **Forms**: Flask-WTF with enhanced validation
- **Internationalization**: Flask-Babel with Estonian and Russian support
- **Icons**: Font Awesome 6
- **Email**: Flask-Mail with SMTP and secure configuration
- **Security**: Enhanced CORS, CSP, and input validation

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

## Recent Fixes and Improvements (ServiceNEW2)

### 🎨 Complete UI/UX Overhaul
- **Updated Color Scheme**: Implemented ServiceNEW2 brand colors (#0f1724, #f97316, #2563eb)
- **Enhanced Typography**: Improved font hierarchy and readability
- **Modern Card Design**: Added glass morphism effects and subtle animations
- **Improved Button Styles**: Enhanced hover effects and loading states
- **Better Visual Feedback**: Added loading animations and status indicators

### 📱 Enhanced Responsiveness & Accessibility
- **Mobile-First Design**: Fully responsive across all device sizes
- **Touch-Friendly Interface**: Optimized touch targets (min 48px)
- **WCAG Compliance**: Screen reader support, keyboard navigation, high contrast mode
- **Semantic HTML**: Proper ARIA labels and semantic structure
- **Skip Navigation**: Accessibility links for keyboard users

### 🔧 Backend Improvements
- **Removed Duplicate API Endpoints**: Fixed routing conflicts in api.py
- **Enhanced Error Handling**: Better logging and user-friendly error messages
- **Input Validation**: Added comprehensive validation for forms and API inputs
- **Security Headers**: Enhanced CORS, CSP, and security configurations
- **Database Improvements**: Better error handling and connection management

### 🌍 Internationalization Enhancements
- **Complete Translation System**: Estonian and Russian language support
- **Flask-Babel Integration**: Proper i18n configuration and compilation
- **Translation Files**: Comprehensive .po/.mo files for both languages
- **Language Switching**: Dynamic locale selection and session management

### 🛠️ Admin Panel Improvements
- **Enhanced Service Approval**: Better visual feedback and confirmation dialogs
- **Improved User Management**: Enhanced handyman approval workflow
- **Better Table Responsiveness**: Mobile-friendly admin tables
- **Loading States**: Visual feedback for all admin actions

### 🎯 Code Quality Improvements
- **Consistent Code Style**: Better organization and maintainability
- **Enhanced Security**: Improved authentication and authorization
- **Better Performance**: Optimized CSS and JavaScript loading
- **Modern CSS**: CSS variables, flexbox, and grid layouts

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