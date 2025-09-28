# Service PRO

Täielik teenuste broneerimise rakendus, mis on ehitatud Python Flaskiga, sisaldades kasutajate registreerimist, admini paneeli, meistrite haldust, modernset reageerivat disaini ja mitmekeelset tuge.

## Funktsioonid

### 🔐 Kasutajate Haldus
- **Kasutajate Registreerimine**: Kliendid saavad süsteemiga registreeruda
- **Rollipõhine Juurdepääs**: Kolm kasutajarolli - Klient, Admin, Meister
- **Turvaline Autentimine**: Paroolide räsimine ja sessioonide haldus
- **Profiili Haldus**: Kasutajad saavad oma profiile hallata

### 🛠️ Teenuste Haldus
- **Teenuste Kataloog**: Adminid saavad saadaval olevaid teenuseid hallata
- **Teenuste Broneerimine**: Kliendid saavad teenuseid internetis broneerida
- **Broneeringute Haldus**: Jälgi broneeringute staatust ja ajalugu
- **Erinõuded**: Kliendid saavad lisada erinõudeid

### 👨‍🔧 Meistrite Süsteem
- **Meistrite Registreerimine**: Professionaalid saavad registreeruda teenuseosutajatena
- **Admini Kinnitamine**: Kõik meistrite registreerimised vajavad admini kinnitust
- **Tööde Määramine**: Adminid määravad tööd kinnitatud meistritele
- **Staatuse Jälgimine**: Meistrid saavad tööde edenemist uuendada

### 🎛️ Admini Paneel
- **Kasutajate Haldus**: Kinnita/tagasi lükka meistrite registreerimised
- **Broneeringute Järelevalve**: Halda kõiki broneeringuid ja määramisi
- **Süsteemi Statistika**: Vaata platvormi kasutusstatistikat
- **Täielik Kontroll**: Täielik administratiivne juurdepääs

### 🌍 Rahvusvahelistamine (i18n)
- **Mitmekeelne Tugi**: Eesti (et) ja vene (ru) keel
- **Flask-Babel Integratsioon**: Täielik tõlkesüsteem
- **Dünaamiline Keele Vahetamine**: Kasutajad saavad keeli vahetada
- **Tõlgitud Sisu**: Kogu UI tekst ja sõnumid on tõlgitud

### 🎨 Modernne Disain & UX
- **Täielikult Reageeriv UI**: Optimeeritud laua-, tahvel- ja mobiiliseadmetele
- **Bootstrap 5**: Modernne, puhas liides täiustatud komponentidega
- **Interaktiivsed Elemendid**: Sujuvad animatsioonid, hover-efektid ja mikro-interaktsioonid
- **Kasutajasõbralik**: Intuitiivne navigeerimine ja sujuvad töövoogud
- **Moderne Avaleht**: Professionaalne kangelase sektsioon, teenuste kaardid, funktsioonide esitlus ja kontaktivorm
- **Klaas Morfismi Efektid**: Modernsed kaardidisainid tausta häguga
- **CSS Muutujad**: Ühtlane teemastamine ServiceNEW2 brändivärvidega
- **Täiustatud Juurdepääsetavus**: WCAG nõuetele vastav koos ekraanilugeja toega, klaviatuuri navigeerimise ja kõrge kontrastiga
- **Laadimise Olekud**: Visuaalne tagasiside kõigile kasutaja tegevustele
- **Puute-sõbralik**: Optimeeritud puute sihtmärgid mobiiliseadmetele

## Tehnoloogia Stack

- **Backend**: Python Flask täiustatud turvalisuse ja veahaldusega
- **Andmebaas**: SQLAlchemy ORM SQLite/PostgreSQL/MySQL toega
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript modernsete animatsioonidega
- **Autentimine**: Flask-Login turvalise sessioonide haldusega
- **Vormid**: Flask-WTF täiustatud valideerimisega
- **Rahvusvahelistamine**: Flask-Babel eesti ja vene keele toega
- **Ikoonid**: Font Awesome 6
- **E-post**: Flask-Mail SMTP ja turvalise konfiguratsiooniga
- **Turvalisus**: Täiustatud CORS, CSP ja sisendi valideerimine

## Paigaldamine

1. **Klooni repositoorium**:
   ```bash
   git clone <repository-url>
   cd service-app
   ```

2. **Loo virtuaalne keskkond**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windowsis: venv\\Scripts\\activate
   ```

3. **Paigalda sõltuvused**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigureeri keskkonnamuutujad**:
   - Kopeeri `.env` fail ja uuenda oma seadetega:
   ```bash
   cp .env .env.local  # Loo koopia
   # Muuda .env.local oma e-posti mandaatide ja andmebaasi seadetega
   ```

5. **Seadista andmebaas** (vali üks valik):

   **Valik A: SQLite (vaikimisi, aga võib olla Windowsi ühilduvusprobleeme)**
   ```bash
   python create_working_db.py
   ```

   **Valik B: PostgreSQL (soovitatav tootmiseks)**
   ```bash
   # Paigalda PostgreSQL ja loo andmebaas esmalt
   # Uuenda .env PostgreSQL ühendusstringiga
   SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/service_pro
   # Seejärel käivita:
   python setup_postgresql.py
   ```

   **Valik C: MySQL (alternatiivne valik)**
   ```bash
   # Paigalda MySQL ja loo andmebaas esmalt
   # Uuenda .env MySQL ühendusstringiga
   SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost:3306/service_pro
   # Seejärel käivita:
   python setup_postgresql.py
   ```

5. **Käivita rakendus**:
   ```bash
   python app.py
   ```

6. **Ava oma brauser**:
   Navigeeri `http://localhost:5000`

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

## Litsents

See projekt on litsentseeritud MIT Litsentsi alusel - vaata LICENSE faili detailide jaoks.

## Tugi

Toe ja küsimuste korral võta palun ühendust arendustiimiga või loo issue repositooriumis.

---

**Ehitatud ❤️ Python Flaskiga**