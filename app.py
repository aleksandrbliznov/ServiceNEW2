from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_babel import Babel, gettext, ngettext, lazy_gettext
from flask_mail import Mail, Message
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, FloatField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API blueprint functions

# Create Flask app
app = Flask(__name__)

# Security: Generate a secure secret key if not provided
def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    import secrets
    return secrets.token_hex(32)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', generate_secret_key())
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/service_app.db')

# Configure engine options based on database type
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
if db_uri.startswith('sqlite'):
    # SQLite-specific options
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'check_same_thread': False}
    }
else:
    # PostgreSQL/MySQL options (no check_same_thread)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['BABEL_DEFAULT_LOCALE'] = os.getenv('BABEL_DEFAULT_LOCALE', 'et')
app.config['BABEL_SUPPORTED_LOCALES'] = os.getenv('BABEL_SUPPORTED_LOCALES', 'et,en').split(',')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'your-email@gmail.com')

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# CORS headers for React frontend
@app.after_request
def add_cors_headers(response):
    """Add CORS and security headers"""
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https: http://localhost:3000; connect-src 'self' http://localhost:5000"
    return response

# Locale selector function
def get_locale():
    # Check if user has a language preference in session
    if 'lang' in session:
        return session['lang']

    # Default to Estonian for now to avoid language detection issues
    return 'et'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
babel = Babel(app, locale_selector=get_locale)

# API Routes for React Frontend
@app.route('/api/service-groups')
def api_get_service_groups():
    """Get all active service groups"""
    try:
        service_groups = ServiceGroup.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': sg.id,
                'name': sg.name,
                'name_et': sg.name_et,
                'name_en': sg.name_en,
                'name_ru': sg.name_ru,
                'description': sg.description,
                'created_at': sg.created_at.isoformat() if sg.created_at else None
            } for sg in service_groups]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/services')
def api_get_services():
    """Get services, optionally filtered by group"""
    try:
        # For public API, show only approved services
        query = Service.query.filter_by(is_active=True, is_approved=True)
        services = query.all()

        return jsonify({
            'success': True,
            'data': [{
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'price': float(s.price),
                'duration_hours': s.duration_hours,
                'category': s.category,
                'service_group_id': s.service_group_id,
                'handyman_id': s.handyman_id,
                'is_active': s.is_active,
                'is_approved': s.is_approved,
                'example_images': json.loads(s.example_images) if s.example_images else [],
                'created_at': s.created_at.isoformat() if s.created_at else None,
                'updated_at': s.updated_at.isoformat() if s.updated_at else None,
                'service_group': {
                    'id': s.service_group.id,
                    'name': s.service_group.name
                } if s.service_group else None,
                'handyman': {
                    'id': s.handyman.id,
                    'first_name': s.handyman.first_name,
                    'last_name': s.handyman.last_name,
                    'average_score': float(s.handyman.average_score) if s.handyman.average_score else 0
                } if s.handyman else None
            } for s in services]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API login endpoint for React frontend"""
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        # Find user by email instead of username for API
        user = User.query.filter_by(email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            login_user(user)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone,
                    'role': user.role,
                    'is_approved': user.is_approved,
                    'average_score': float(user.average_score) if user.average_score else 0,
                    'total_feedbacks': user.total_feedbacks
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': 'Login failed', 'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """API registration endpoint for React frontend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'}), 409

        existing_username = User.query.filter_by(username=data.get('username', data.get('email'))).first()
        if existing_username:
            return jsonify({'success': False, 'message': 'Username already exists'}), 409

        user = User(
            username=data.get('username', data.get('email')),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone', ''),
            role=data.get('role', 'customer')
        )
        user.set_password(data.get('password'))
        user.is_approved = True  # Auto-approve for now

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed', 'error': str(e)}), 500

@app.route('/api/auth/logout')
def api_logout():
    """API logout endpoint"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/me')
@login_required
def api_get_current_user():
    """Get current user information"""
    return jsonify({
        'success': True,
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone': current_user.phone,
            'role': current_user.role,
            'is_approved': current_user.is_approved,
            'average_score': float(current_user.average_score) if current_user.average_score else 0,
            'total_feedbacks': current_user.total_feedbacks
        }
    })

# Make translation function available in templates
@app.context_processor
def inject_gettext():
    return {
        '_': gettext
    }

# User roles
USER = 'user'
ADMIN = 'admin'
HANDYMAN = 'handyman'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default=USER)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=True)  # Auto-approve for now
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    average_score = db.Column(db.Float, default=0.0)
    total_feedbacks = db.Column(db.Integer, default=0)
    admin_approved = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        """Generate a password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token):
        """Verify if the reset token is valid"""
        return (self.reset_token == token and
                self.reset_token_expiry and
                self.reset_token_expiry > datetime.utcnow())

    def clear_reset_token(self):
        """Clear the reset token"""
        self.reset_token = None
        self.reset_token_expiry = None

    def update_score(self):
        """Update average score based on feedback"""
        if self.role == HANDYMAN:
            feedbacks = Feedback.query.filter_by(handyman_id=self.id).all()
            if feedbacks:
                total_score = sum(f.rating for f in feedbacks)
                self.average_score = total_score / len(feedbacks)
                self.total_feedbacks = len(feedbacks)
            else:
                self.average_score = 0.0
                self.total_feedbacks = 0

class ServiceGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_et = db.Column(db.String(100))  # Estonian name
    name_en = db.Column(db.String(100))  # English name
    name_ru = db.Column(db.String(100))  # Russian name
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_hours = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    service_group_id = db.Column(db.Integer, db.ForeignKey('service_group.id'), nullable=False)
    handyman_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    example_images = db.Column(db.Text)  # JSON string of image paths
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service_group = db.relationship('ServiceGroup', backref='services')
    handyman = db.relationship('User', foreign_keys=[handyman_id])

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    handyman_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    special_requests = db.Column(db.Text)
    total_price = db.Column(db.Float, nullable=False)
    admin_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id])
    service = db.relationship('Service')
    handyman = db.relationship('User', foreign_keys=[handyman_id])

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    handyman_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking')
    user = db.relationship('User', foreign_keys=[user_id])
    handyman = db.relationship('User', foreign_keys=[handyman_id])

class WorkHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handyman_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    handyman = db.relationship('User', foreign_keys=[handyman_id])

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    handyman_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_price = db.Column(db.Float, nullable=False)
    commission_amount = db.Column(db.Float, nullable=False)  # 10% of service_price
    handyman_earnings = db.Column(db.Float, nullable=False)  # 90% of service_price
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking')
    handyman = db.relationship('User', foreign_keys=[handyman_id])

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Forms
class RegistrationForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    first_name = StringField(lazy_gettext('First Name'), validators=[DataRequired()])
    last_name = StringField(lazy_gettext('Last Name'), validators=[DataRequired()])
    phone = StringField(lazy_gettext('Phone'), validators=[DataRequired()])
    role = SelectField(lazy_gettext('I want to register as'), choices=[
        (USER, lazy_gettext('Customer')),
        (HANDYMAN, lazy_gettext('Service Provider'))
    ], validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Login'))

class ServiceForm(FlaskForm):
    name = StringField(lazy_gettext('Service Name'), validators=[DataRequired()])
    description = TextAreaField(lazy_gettext('Description'), validators=[DataRequired()])
    price = FloatField(lazy_gettext('Price'), validators=[DataRequired(), NumberRange(min=0)])
    duration_hours = IntegerField(lazy_gettext('Duration (hours)'), validators=[DataRequired(), NumberRange(min=1)])
    category = SelectField(lazy_gettext('Category'), choices=[
        ('Plumbing', lazy_gettext('Plumbing')),
        ('Electrical', lazy_gettext('Electrical')),
        ('Cleaning', lazy_gettext('Cleaning')),
        ('Gardening', lazy_gettext('Gardening')),
        ('Painting', lazy_gettext('Painting')),
        ('Carpentry', lazy_gettext('Carpentry')),
        ('Other', lazy_gettext('Other'))
    ], validators=[DataRequired()])
    service_group_id = SelectField(lazy_gettext('Service Group'), coerce=int, validators=[DataRequired()])

class BookingForm(FlaskForm):
    service_id = SelectField(lazy_gettext('Service'), coerce=int)
    booking_date = StringField(lazy_gettext('Preferred Date & Time'), validators=[DataRequired()])
    special_requests = TextAreaField(lazy_gettext('Special Requests'))

class FeedbackForm(FlaskForm):
    rating = SelectField(lazy_gettext('Rating'), choices=[
        (5, lazy_gettext('5 Stars - Excellent')),
        (4, lazy_gettext('4 Stars - Very Good')),
        (3, lazy_gettext('3 Stars - Good')),
        (2, lazy_gettext('2 Stars - Fair')),
        (1, lazy_gettext('1 Star - Poor'))
    ], coerce=int, validators=[DataRequired()])
    comment = TextAreaField(lazy_gettext('Comment'), validators=[Length(max=500)])

class PasswordResetRequestForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(lazy_gettext('Send Reset Link'))

class PasswordResetForm(FlaskForm):
    password = PasswordField(lazy_gettext('New Password'), validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(lazy_gettext('Confirm New Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(lazy_gettext('Reset Password'))

class UserEditForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(lazy_gettext('First Name'), validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(lazy_gettext('Last Name'), validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField(lazy_gettext('Phone'), validators=[DataRequired(), Length(min=10, max=20)])
    submit = SubmitField(lazy_gettext('Update User'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.user_id:
            raise ValidationError('Email already registered to another user.')

class ServiceGroupForm(FlaskForm):
    name = StringField(lazy_gettext('Group Name'), validators=[DataRequired(), Length(min=2, max=100)])
    name_et = StringField(lazy_gettext('Group Name (Estonian)'), validators=[Length(max=100)])
    name_en = StringField(lazy_gettext('Group Name (English)'), validators=[Length(max=100)])
    name_ru = StringField(lazy_gettext('Group Name (Russian)'), validators=[Length(max=100)])
    description = TextAreaField(lazy_gettext('Description'))
    submit = SubmitField(lazy_gettext('Save Group'))

class HandymanServiceForm(FlaskForm):
    name = StringField(lazy_gettext('Service Name'), validators=[DataRequired()])
    description = TextAreaField(lazy_gettext('Description'), validators=[DataRequired()])
    price = FloatField(lazy_gettext('Price'), validators=[DataRequired(), NumberRange(min=0)])
    duration_hours = IntegerField(lazy_gettext('Duration (hours)'), validators=[DataRequired(), NumberRange(min=1)])
    service_group_id = SelectField(lazy_gettext('Service Group'), coerce=int, validators=[DataRequired()])
    example_images = TextAreaField(lazy_gettext('Example Image URLs (one per line)'))
    submit = SubmitField(lazy_gettext('Add Service'))

class WorkHoursForm(FlaskForm):
    day_of_week = SelectField(lazy_gettext('Day'), choices=[
        (0, lazy_gettext('Monday')),
        (1, lazy_gettext('Tuesday')),
        (2, lazy_gettext('Wednesday')),
        (3, lazy_gettext('Thursday')),
        (4, lazy_gettext('Friday')),
        (5, lazy_gettext('Saturday')),
        (6, lazy_gettext('Sunday'))
    ], coerce=int, validators=[DataRequired()])
    start_time = StringField(lazy_gettext('Start Time'), validators=[DataRequired()])
    end_time = StringField(lazy_gettext('End Time'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Save Hours'))

# Routes
@app.route('/')
def index():
    try:
        # Check if modern landing page exists and serve it
        import os
        landing_template = 'landing.html'
        index_template = 'index.html'

        # Try to serve landing page first
        if os.path.exists(os.path.join(app.root_path, 'templates', landing_template)):
            service_groups = ServiceGroup.query.filter_by(is_active=True).limit(6).all()
            return render_template(landing_template, service_groups=service_groups)
        # Fallback to original index page
        elif os.path.exists(os.path.join(app.root_path, 'templates', index_template)):
            service_groups = ServiceGroup.query.filter_by(is_active=True).limit(6).all()
            return render_template(index_template, service_groups=service_groups)
        # Ultimate fallback - simple message
        else:
            return '''
            <html>
            <head><title>Service PRO - Handyman Services</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>Service PRO</h1>
                <p>Professional handyman services at your fingertips.</p>
                <p><a href="/register">Register</a> | <a href="/login">Login</a></p>
            </body>
            </html>
            '''
    except Exception as e:
        print(f"Error loading index: {e}")
        # Fallback to simple message on error
        return '''
        <html>
        <head><title>Service PRO - Handyman Services</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>Service PRO</h1>
            <p>Professional handyman services at your fingertips.</p>
            <p><a href="/register">Register</a> | <a href="/login">Login</a></p>
        </body>
        </html>
        '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data,
                role=form.role.data
            )
            user.set_password(form.password.data)
            user.is_approved = True  # Auto-approve for now

            db.session.add(user)
            db.session.commit()

            flash('Registreerimine õnnestus! Palun logige sisse.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            print(f"Registration error: {e}")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Sisselogimine õnnestus!', 'success')

                if user.role == ADMIN:
                    return redirect(url_for('admin_dashboard'))
                elif user.role == HANDYMAN:
                    return redirect(url_for('handyman_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        except Exception as e:
            flash('Login failed. Please try again.', 'error')
            print(f"Login error: {e}")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Olete välja logitud.', 'info')
    return redirect(url_for('index'))

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != USER:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return render_template('user_dashboard.html', bookings=bookings)
    except Exception as e:
        print(f"Error loading user dashboard: {e}")
        return render_template('user_dashboard.html', bookings=[])

@app.route('/services')
@login_required
def services():
    """Display all service groups for customers to choose from"""
    if current_user.role != USER:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        service_groups = ServiceGroup.query.filter_by(is_active=True).all()
        return render_template('services.html', service_groups=service_groups)
    except Exception as e:
        print(f"Error loading services: {e}")
        return render_template('services.html', service_groups=[])

@app.route('/services/group/<int:group_id>')
@login_required
def services_by_group(group_id):
    """Display services within a specific group"""
    if current_user.role != USER:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        service_group = ServiceGroup.query.get_or_404(group_id)
        services = Service.query.filter_by(
            service_group_id=group_id,
            is_active=True,
            is_approved=True
        ).all()
        return render_template('services_by_group.html', service_group=service_group, services=services)
    except Exception as e:
        print(f"Error loading services by group: {e}")
        return redirect(url_for('services'))

@app.route('/user/book/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book_service(service_id):
    if current_user.role != USER:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        service = Service.query.get_or_404(service_id)

        # Verify service is approved and active
        if not service.is_approved or not service.is_active:
            flash('Service is not available for booking.', 'error')
            return redirect(url_for('services'))

        form = BookingForm()

        if form.validate_on_submit():
            try:
                # Handle datetime-local format from HTML input
                booking_date_str = form.booking_date.data
                if not booking_date_str:
                    flash('Please select a valid date and time.', 'error')
                    return render_template('book_service.html', form=form, service=service)

                try:
                    # Try parsing as datetime-local format (YYYY-MM-DDTHH:MM)
                    booking_date = datetime.strptime(booking_date_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    try:
                        # If that fails, try with seconds (YYYY-MM-DDTHH:MM:SS)
                        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        flash('Invalid date/time format. Please use the calendar picker.', 'error')
                        return render_template('book_service.html', form=form, service=service)

                # Validate that booking date is in the future
                if booking_date <= datetime.now():
                    flash('Please select a future date and time.', 'error')
                    return render_template('book_service.html', form=form, service=service)

                booking = Booking(
                    user_id=current_user.id,
                    service_id=service_id,
                    booking_date=booking_date,
                    special_requests=form.special_requests.data,
                    total_price=service.price,
                    status='pending'
                )

                db.session.add(booking)
                db.session.commit()

                # Calculate and create commission record
                commission_amount = service.price * 0.10  # 10% commission
                handyman_earnings = service.price * 0.90  # 90% to handyman

                commission = Commission(
                    booking_id=booking.id,
                    handyman_id=service.handyman_id,
                    service_price=service.price,
                    commission_amount=commission_amount,
                    handyman_earnings=handyman_earnings
                )
                db.session.add(commission)
                db.session.commit()

                # Send email notifications
                try:
                    # Notify user
                    user_msg = Message(_('Booking Confirmation - Service PRO'),
                                      sender=app.config['MAIL_DEFAULT_SENDER'],
                                      recipients=[current_user.email])
                    user_msg.body = f'''{_('Dear')} {current_user.first_name},

{_('Your booking has been placed successfully!')}

{_('Booking Details:')}
- {_('Service:')} {service.name}
- {_('Provider:')} {service.handyman.first_name} {service.handyman.last_name}
- {_('Date & Time:')} {booking_date.strftime('%Y-%m-%d %H:%M')}
- {_('Price:')} ${service.price}
- {_('Status: Pending approval')}

{_('You will receive another email once your booking is confirmed.')}

{_('Thank you for using Service PRO!')}
'''
                    mail.send(user_msg)

                    # Notify handyman
                    handyman_msg = Message(_('New Booking - Service PRO'),
                                          sender=app.config['MAIL_DEFAULT_SENDER'],
                                          recipients=[service.handyman.email])
                    handyman_msg.body = f'''{_('New booking for your service!')}

{_('Customer:')} {current_user.first_name} {current_user.last_name}
{_('Service:')} {service.name}
{_('Date & Time:')} {booking_date.strftime('%Y-%m-%d %H:%M')}
{_('Price:')} ${service.price}

{_('Please check your dashboard for details.')}
'''
                    mail.send(handyman_msg)

                    # Notify admin
                    admin_users = User.query.filter_by(role=ADMIN).all()
                    for admin in admin_users:
                        admin_msg = Message(_('New Booking Placed - Service PRO'),
                                          sender=app.config['MAIL_DEFAULT_SENDER'],
                                          recipients=[admin.email])
                        admin_msg.body = f'''{_('New booking has been placed:')}

{_('Customer:')} {current_user.first_name} {current_user.last_name}
{_('Service:')} {service.name}
{_('Provider:')} {service.handyman.first_name} {service.handyman.last_name}
{_('Date & Time:')} {booking_date.strftime('%Y-%m-%d %H:%M')}
{_('Price:')} ${service.price}

{_('Commission:')} ${commission_amount}
{_('Handyman Earnings:')} ${handyman_earnings}
'''
                        mail.send(admin_msg)

                except Exception as e:
                    print(f"Email notification error: {e}")
                    # Don't fail the booking if email fails

                flash('Teenus broneeritud edukalt!', 'success')
                return redirect(url_for('user_dashboard'))
            except Exception as e:
                db.session.rollback()
                flash('Broneerimine ebaõnnestus. Palun proovige uuesti.', 'error')
                print(f"Booking error: {e}")

        return render_template('book_service.html', form=form, service=service)
    except Exception as e:
        flash('Teenust ei leitud.', 'error')
        return redirect(url_for('services'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        total_users = User.query.count()
        total_services = Service.query.filter_by(is_approved=True).count()
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        pending_handymen = User.query.filter_by(role=HANDYMAN, is_approved=False).count()
        pending_services_count = Service.query.filter_by(is_approved=False).count()
        total_service_groups = ServiceGroup.query.filter_by(is_active=True).count()

        # Get handyman statistics for dashboard
        approved_handymen = User.query.filter_by(role=HANDYMAN, is_approved=True).all()
        total_earnings = 0
        in_progress_jobs = 0
        completed_jobs = 0

        for handyman in approved_handymen:
            bookings = Booking.query.filter_by(handyman_id=handyman.id).all()
            total_earnings += sum(booking.total_price for booking in bookings if booking.status == 'completed')
            in_progress_jobs += len([b for b in bookings if b.status == 'in_progress'])
            completed_jobs += len([b for b in bookings if b.status == 'completed'])

        # Calculate commission statistics
        total_commissions = Commission.query.filter_by(is_paid=False).all()
        total_commission_amount = sum(c.commission_amount for c in total_commissions)
        total_handyman_earnings = sum(c.handyman_earnings for c in total_commissions)

        return render_template('admin_dashboard.html',
                             total_users=total_users,
                             total_services=total_services,
                             total_bookings=total_bookings,
                             pending_bookings=pending_bookings,
                             pending_handymen=pending_handymen,
                             pending_services_count=pending_services_count,
                             total_service_groups=total_service_groups,
                             total_earnings=total_earnings,
                             in_progress_jobs=in_progress_jobs,
                             completed_jobs=completed_jobs,
                             approved_handymen_count=len(approved_handymen),
                             total_commission_amount=total_commission_amount,
                             total_handyman_earnings=total_handyman_earnings)
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        return render_template('admin_dashboard.html',
                             total_users=0,
                             total_services=0,
                             total_bookings=0,
                             pending_bookings=0,
                             pending_handymen=0,
                             pending_services_count=0,
                             total_service_groups=0,
                             total_earnings=0,
                             in_progress_jobs=0,
                             completed_jobs=0,
                             approved_handymen_count=0,
                             total_commission_amount=0,
                             total_handyman_earnings=0)

@app.route('/admin/services')
@login_required
def admin_services():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        services = Service.query.all()
        return render_template('admin_services.html', services=services)
    except Exception as e:
        print(f"Error loading admin services: {e}")
        return render_template('admin_services.html', services=[])

@app.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    form = ServiceForm()

    # Populate service group choices
    service_groups = ServiceGroup.query.filter_by(is_active=True).all()
    form.service_group_id.choices = [(g.id, g.name) for g in service_groups]

    if form.validate_on_submit():
        try:
            service = Service(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                duration_hours=form.duration_hours.data,
                category=form.category.data,
                service_group_id=form.service_group_id.data,
                handyman_id=current_user.id  # Admin creates services for themselves
            )
            db.session.add(service)
            db.session.commit()
            flash('Teenus lisatud edukalt!', 'success')
            return redirect(url_for('admin_services'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add service. Please try again.', 'error')
            print(f"Add service error: {e}")

    return render_template('add_service.html', form=form)

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        bookings = Booking.query.all()
        return render_template('admin_bookings.html', bookings=bookings)
    except Exception as e:
        print(f"Error loading admin bookings: {e}")
        return render_template('admin_bookings.html', bookings=[])

@app.route('/admin/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)
    form = ServiceForm()

    if form.validate_on_submit():
        try:
            service.name = form.name.data
            service.description = form.description.data
            service.price = form.price.data
            service.duration_hours = form.duration_hours.data
            service.category = form.category.data
            db.session.commit()
            flash('Teenus uuendatud edukalt!', 'success')
            return redirect(url_for('admin_services'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update service. Please try again.', 'error')
            print(f"Update service error: {e}")

    # Pre-populate form with existing service data
    if request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.price.data = service.price
        form.duration_hours.data = service.duration_hours
        form.category.data = service.category

    return render_template('edit_service.html', form=form, service=service)

@app.route('/admin/services/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)

    try:
        db.session.delete(service)
        db.session.commit()
        flash('Teenus kustutatud edukalt!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete service. Please try again.', 'error')
        print(f"Delete service error: {e}")

    return redirect(url_for('admin_services'))
    
    # Enhanced Admin Booking Management
@app.route('/admin/bookings/approve/<int:booking_id>', methods=['POST'])
@login_required
def approve_booking(booking_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)
    booking.admin_approved = True
    booking.status = 'approved'
    db.session.commit()
    flash('Booking approved successfully!', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/bookings/decline/<int:booking_id>')
@login_required
def decline_booking(booking_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)
    booking.admin_approved = False
    booking.status = 'declined'
    db.session.commit()
    flash('Booking declined.', 'info')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/approve_handyman/<int:user_id>')
@login_required
def approve_handyman(user_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    user = User.query.get_or_404(user_id)
    if user.role == HANDYMAN:
        user.is_approved = True
        db.session.commit()
        flash(f'Handyman {user.username} has been approved.', 'success')

    return redirect(url_for('admin_users'))

@app.route('/admin/assign_handyman/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def assign_handyman(booking_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)
    available_handymen = User.query.filter_by(role=HANDYMAN, is_approved=True).all()

    if request.method == 'POST':
        handyman_id = request.form.get('handyman_id')
        if handyman_id:
            booking.handyman_id = handyman_id
            booking.status = 'approved'
            db.session.commit()
            flash('Handyman assigned and booking approved.', 'success')
            return redirect(url_for('admin_bookings'))

    return render_template('assign_handyman.html', booking=booking, handymen=available_handymen)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        users = User.query.all()
        # Get handyman statistics for display
        handyman_stats = []
        handymen = User.query.filter_by(role=HANDYMAN, is_approved=True).all()
        for handyman in handymen:
            # Get bookings for this handyman
            bookings = Booking.query.filter_by(handyman_id=handyman.id).all()

            # Calculate statistics
            total_earnings = sum(booking.total_price for booking in bookings if booking.status == 'completed')
            in_progress_count = len([b for b in bookings if b.status == 'in_progress'])
            completed_count = len([b for b in bookings if b.status == 'completed'])

            handyman_stats.append({
                'handyman': handyman,
                'total_earnings': total_earnings,
                'in_progress': in_progress_count,
                'completed': completed_count,
                'total_jobs': len(bookings)
            })

        return render_template('admin_users.html', users=users, handyman_stats=handyman_stats)
    except Exception as e:
        print(f"Error loading admin users: {e}")
        return render_template('admin_users.html', users=[], handyman_stats=[])

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    user = User.query.get_or_404(user_id)
    form = UserEditForm()

    # Store user_id in form for validation
    form.user_id = user_id

    if form.validate_on_submit():
        try:
            # Check if email changed and is already taken by another user
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user and existing_user.id != user_id:
                flash('Email already registered to another user.', 'error')
                return render_template('edit_user.html', form=form, user=user)

            # Update user information
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.phone = form.phone.data

            db.session.commit()
            flash(f'User {user.username} has been updated successfully!', 'success')
            return redirect(url_for('admin_users'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating user. Please try again.', 'error')
            print(f"Update user error: {e}")

    # Pre-populate form with existing user data
    if request.method == 'GET':
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.phone.data = user.phone

    return render_template('edit_user.html', form=form, user=user)

@app.route('/handyman/dashboard')
@login_required
def handyman_dashboard():
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        bookings = Booking.query.filter_by(handyman_id=current_user.id).all()
        return render_template('handyman_dashboard.html', bookings=bookings)
    except Exception as e:
        print(f"Error loading handyman dashboard: {e}")
        return render_template('handyman_dashboard.html', bookings=[])

@app.route('/handyman/update-booking-status/<int:booking_id>', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    """Update booking status (for handyman use)"""
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)

    # Check if this booking is assigned to current handyman
    if booking.handyman_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('handyman_dashboard'))

    new_status = request.form.get('status')
    if new_status in ['in_progress', 'completed']:
        booking.status = new_status
        db.session.commit()
        flash('Broneeringu staatus uuendatud!', 'success')
    else:
        flash('Invalid status.', 'error')

    return redirect(url_for('handyman_dashboard'))

@app.route('/leave-feedback/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def leave_feedback(booking_id):
    if current_user.role != USER:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)

    # Check if user owns this booking and if it's completed
    if booking.user_id != current_user.id or booking.status != 'completed':
        flash('Invalid booking or booking not completed yet.', 'error')
        return redirect(url_for('user_dashboard'))

    # Check if feedback already exists
    existing_feedback = Feedback.query.filter_by(booking_id=booking_id).first()
    if existing_feedback:
        flash('You have already left feedback for this booking.', 'info')
        return redirect(url_for('user_dashboard'))

    form = FeedbackForm()
    if form.validate_on_submit():
        try:
            feedback = Feedback(
                booking_id=booking_id,
                user_id=current_user.id,
                handyman_id=booking.handyman_id,
                rating=form.rating.data,
                comment=form.comment.data
            )
            db.session.add(feedback)
            db.session.commit()

            # Update handyman's score
            handyman = booking.handyman
            handyman.update_score()
            db.session.commit()

            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('user_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting feedback. Please try again.', 'error')
            print(f"Feedback error: {e}")

    return render_template('leave_feedback.html', form=form, booking=booking)

@app.route('/handyman/feedback')
@login_required
def handyman_feedback():
    """Show handyman their feedback"""
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        # Get all feedback for this handyman with related data
        feedbacks = Feedback.query.filter_by(handyman_id=current_user.id).all()

        # Calculate statistics
        total_feedbacks = len(feedbacks)
        avg_rating = 0.0
        five_star_count = 0
        four_plus_count = 0

        if feedbacks:
            ratings = [f.rating for f in feedbacks]
            avg_rating = sum(ratings) / len(ratings)
            five_star_count = len([r for r in ratings if r == 5])
            four_plus_count = len([r for r in ratings if r >= 4])

        # Debug: Print feedback count
        print(f"Found {total_feedbacks} feedback records for handyman {current_user.id}")

        return render_template('handyman_feedback.html',
                             feedbacks=feedbacks,
                             total_feedbacks=total_feedbacks,
                             avg_rating=avg_rating,
                             five_star_count=five_star_count,
                             four_plus_count=four_plus_count)
    except Exception as e:
        print(f"Error loading handyman feedback: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading feedback. Please try again.', 'error')
        return redirect(url_for('handyman_dashboard'))

@app.route('/password-reset-request', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                # Generate reset token
                token = user.generate_reset_token()
                db.session.commit()

                # Send email
                reset_url = url_for('password_reset', token=token, _external=True)
                msg = Message(_('Password Reset Request'),
                             sender=app.config['MAIL_DEFAULT_SENDER'],
                             recipients=[user.email])
                msg.body = f'''{_('To reset your password, visit the following link:')}
{reset_url}

{_('If you did not make this request, simply ignore this email.')}
'''
                mail.send(msg)

                flash(_('Password reset instructions have been sent to your email.'), 'info')
                return redirect(url_for('login'))
            else:
                flash(_('If an account with that email exists, a password reset link has been sent.'), 'info')
                return redirect(url_for('login'))
        except Exception as e:
            flash(_('Error sending email. Please try again later.'), 'error')
            print(f"Email error: {e}")

    return render_template('password_reset_request.html', form=form)

@app.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    try:
        user = User.query.filter_by(reset_token=token).first()
        if not user or not user.verify_reset_token(token):
            flash(_('Invalid or expired reset token.'), 'error')
            return redirect(url_for('password_reset_request'))
    except:
        flash(_('Invalid reset token.'), 'error')
        return redirect(url_for('password_reset_request'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        try:
            user.set_password(form.password.data)
            user.clear_reset_token()
            db.session.commit()

            flash(_('Your password has been updated!'), 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(_('Error updating password. Please try again.'), 'error')
            print(f"Password update error: {e}")

    return render_template('password_reset.html', form=form, token=token)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    if current_user.id == user_id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))

    user = User.query.get_or_404(user_id)

    try:
        # Delete user's feedback
        Feedback.query.filter_by(user_id=user_id).delete()
        Feedback.query.filter_by(handyman_id=user_id).delete()

        # Delete user's bookings
        Booking.query.filter_by(user_id=user_id).delete()

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        flash(f'User {user.username} has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user. Please try again.', 'error')
        print(f"Delete user error: {e}")

    return redirect(url_for('admin_users'))

# Service Group Management Routes
@app.route('/admin/service-groups')
@login_required
def admin_service_groups():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        service_groups = ServiceGroup.query.filter_by(is_active=True).all()
        return render_template('admin_service_groups.html', service_groups=service_groups)
    except Exception as e:
        print(f"Error loading service groups: {e}")
        return render_template('admin_service_groups.html', service_groups=[])

@app.route('/admin/service-groups/add', methods=['GET', 'POST'])
@login_required
def add_service_group():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    form = ServiceGroupForm()
    if form.validate_on_submit():
        try:
            service_group = ServiceGroup(
                name=form.name.data,
                name_et=form.name_et.data or form.name.data,
                name_en=form.name_en.data or form.name.data,
                name_ru=form.name_ru.data or form.name.data,
                description=form.description.data
            )
            db.session.add(service_group)
            db.session.commit()
            flash('Service group added successfully!', 'success')
            return redirect(url_for('admin_service_groups'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add service group. Please try again.', 'error')
            print(f"Add service group error: {e}")

    return render_template('add_service_group.html', form=form)

@app.route('/admin/service-groups/edit/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_service_group(group_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service_group = ServiceGroup.query.get_or_404(group_id)
    form = ServiceGroupForm()

    if form.validate_on_submit():
        try:
            service_group.name = form.name.data
            service_group.name_et = form.name_et.data or form.name.data
            service_group.name_en = form.name_en.data or form.name.data
            service_group.name_ru = form.name_ru.data or form.name.data
            service_group.description = form.description.data
            db.session.commit()
            flash('Service group updated successfully!', 'success')
            return redirect(url_for('admin_service_groups'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update service group. Please try again.', 'error')
            print(f"Update service group error: {e}")

    # Pre-populate form with existing data
    if request.method == 'GET':
        form.name.data = service_group.name
        form.name_et.data = service_group.name_et
        form.name_en.data = service_group.name_en
        form.name_ru.data = service_group.name_ru
        form.description.data = service_group.description

    return render_template('edit_service_group.html', form=form, service_group=service_group)

@app.route('/admin/service-groups/delete/<int:group_id>', methods=['POST'])
@login_required
def delete_service_group(group_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service_group = ServiceGroup.query.get_or_404(group_id)

    try:
        db.session.delete(service_group)
        db.session.commit()
        flash('Service group deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete service group. Please try again.', 'error')
        print(f"Delete service group error: {e}")

    return redirect(url_for('admin_service_groups'))

# Handyman Service Management Routes
@app.route('/handyman/services')
@login_required
def handyman_services():
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        services = Service.query.filter_by(handyman_id=current_user.id).all()
        return render_template('handyman_services.html', services=services)
    except Exception as e:
        print(f"Error loading handyman services: {e}")
        return render_template('handyman_services.html', services=[])

@app.route('/handyman/services/add', methods=['GET', 'POST'])
@login_required
def add_handyman_service():
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    form = HandymanServiceForm()

    # Populate service group choices
    service_groups = ServiceGroup.query.filter_by(is_active=True).all()
    form.service_group_id.choices = [(g.id, g.name) for g in service_groups]

    if form.validate_on_submit():
        try:
            # Handle example images
            image_urls = []
            if form.example_images.data:
                image_urls = [url.strip() for url in form.example_images.data.split('\n') if url.strip()]

            service = Service(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                duration_hours=form.duration_hours.data,
                service_group_id=form.service_group_id.data,
                handyman_id=current_user.id,
                example_images=json.dumps(image_urls) if image_urls else None
            )
            db.session.add(service)
            db.session.commit()
            flash('Service added successfully! Waiting for admin approval.', 'success')
            return redirect(url_for('handyman_services'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add service. Please try again.', 'error')
            print(f"Add handyman service error: {e}")

    return render_template('add_handyman_service.html', form=form)

@app.route('/handyman/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_handyman_service(service_id):
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)

    # Check if this service belongs to current handyman
    if service.handyman_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('handyman_services'))

    form = HandymanServiceForm()

    # Populate service group choices
    service_groups = ServiceGroup.query.filter_by(is_active=True).all()
    form.service_group_id.choices = [(g.id, g.name) for g in service_groups]

    if form.validate_on_submit():
        try:
            # Handle example images
            image_urls = []
            if form.example_images.data:
                image_urls = [url.strip() for url in form.example_images.data.split('\n') if url.strip()]

            service.name = form.name.data
            service.description = form.description.data
            service.price = form.price.data
            service.duration_hours = form.duration_hours.data
            service.service_group_id = form.service_group_id.data
            service.example_images = json.dumps(image_urls) if image_urls else None
            service.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Service updated successfully!', 'success')
            return redirect(url_for('handyman_services'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update service. Please try again.', 'error')
            print(f"Update handyman service error: {e}")

    # Pre-populate form with existing data
    if request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.price.data = service.price
        form.duration_hours.data = service.duration_hours
        form.service_group_id.data = service.service_group_id
        if service.example_images:
            images = json.loads(service.example_images)
            form.example_images.data = '\n'.join(images)

    return render_template('edit_handyman_service.html', form=form, service=service)

@app.route('/handyman/services/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_handyman_service(service_id):
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)

    # Check if this service belongs to current handyman
    if service.handyman_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('handyman_services'))

    try:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete service. Please try again.', 'error')
        print(f"Delete handyman service error: {e}")

    return redirect(url_for('handyman_services'))

# Work Hours Management Routes
@app.route('/handyman/work-hours')
@login_required
def handyman_work_hours():
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        work_hours = WorkHours.query.filter_by(handyman_id=current_user.id).all()
        return render_template('handyman_work_hours.html', work_hours=work_hours)
    except Exception as e:
        print(f"Error loading work hours: {e}")
        return render_template('handyman_work_hours.html', work_hours=[])

@app.route('/handyman/work-hours/add', methods=['GET', 'POST'])
@login_required
def add_work_hours():
    if current_user.role != HANDYMAN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    form = WorkHoursForm()
    if form.validate_on_submit():
        try:
            work_hours = WorkHours(
                handyman_id=current_user.id,
                day_of_week=form.day_of_week.data,
                start_time=datetime.strptime(form.start_time.data, '%H:%M').time(),
                end_time=datetime.strptime(form.end_time.data, '%H:%M').time()
            )
            db.session.add(work_hours)
            db.session.commit()
            flash('Work hours added successfully!', 'success')
            return redirect(url_for('handyman_work_hours'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add work hours. Please try again.', 'error')
            print(f"Add work hours error: {e}")

    return render_template('add_work_hours.html', form=form)

# Admin Service Approval Routes
@app.route('/admin/pending-services')
@login_required
def admin_pending_services():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        pending_services = Service.query.filter_by(is_approved=False).all()
        return render_template('admin_pending_services.html', services=pending_services)
    except Exception as e:
        print(f"Error loading pending services: {e}")
        return render_template('admin_pending_services.html', services=[])

@app.route('/admin/approve-service/<int:service_id>')
@login_required
def approve_service(service_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)
    service.is_approved = True
    db.session.commit()
    flash(f'Service "{service.name}" has been approved.', 'success')
    return redirect(url_for('admin_pending_services'))

@app.route('/admin/reject-service/<int:service_id>')
@login_required
def reject_service(service_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash(f'Service "{service.name}" has been rejected and deleted.', 'info')
    return redirect(url_for('admin_pending_services'))

# Commission Management Routes
@app.route('/admin/commissions')
@login_required
def admin_commissions():
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    try:
        commissions = Commission.query.all()
        total_commission = sum(c.commission_amount for c in commissions if not c.is_paid)
        total_earnings = sum(c.handyman_earnings for c in commissions if not c.is_paid)

        return render_template('admin_commissions.html',
                             commissions=commissions,
                             total_commission=total_commission,
                             total_earnings=total_earnings)
    except Exception as e:
        print(f"Error loading commissions: {e}")
        return render_template('admin_commissions.html', commissions=[], total_commission=0, total_earnings=0)

@app.route('/admin/mark-commission-paid/<int:commission_id>')
@login_required
def mark_commission_paid(commission_id):
    if current_user.role != ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))

    commission = Commission.query.get_or_404(commission_id)
    commission.is_paid = True
    db.session.commit()
    flash('Commission marked as paid.', 'success')
    return redirect(url_for('admin_commissions'))

# Initialize database
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

# Create admin user
@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    try:
        admin = User(
            username='admin',
            email='aleksandr@asbg.ee',
            first_name='Admin',
            last_name='User',
            role=ADMIN,
            is_approved=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created! Username: admin, Password: admin123')
    except Exception as e:
        print(f'Error creating admin: {e}')

# Create initial service groups
@app.cli.command('create-service-groups')
def create_service_groups():
    """Create initial service groups as specified in requirements."""
    try:
        groups_data = [
            {
                'name': 'Kondiiter',
                'name_et': 'Kondiiter',
                'name_en': 'Confectioner',
                'name_ru': 'Кондитер',
                'description': 'Cake making, baking, and confectionery services'
            },
            {
                'name': 'Ehitus',
                'name_et': 'Ehitus',
                'name_en': 'Construction',
                'name_ru': 'Строительство',
                'description': 'Construction, renovation, and building services'
            },
            {
                'name': 'Koristus',
                'name_et': 'Koristus',
                'name_en': 'Cleaning',
                'name_ru': 'Уборка',
                'description': 'Cleaning services for homes and offices'
            },
            {
                'name': 'IT abi',
                'name_et': 'IT abi',
                'name_en': 'IT Support',
                'name_ru': 'IT поддержка',
                'description': 'Computer repair, software installation, and IT support'
            }
        ]

        for group_data in groups_data:
            # Check if group already exists
            existing_group = ServiceGroup.query.filter_by(name=group_data['name']).first()
            if not existing_group:
                group = ServiceGroup(**group_data)
                db.session.add(group)
                print(f'Created service group: {group_data["name"]}')
            else:
                print(f'Service group already exists: {group_data["name"]}')

        db.session.commit()
        print('Initial service groups created successfully!')
    except Exception as e:
        print(f'Error creating service groups: {e}')

if __name__ == '__main__':
    with app.app_context():
        try:
            # Test database connection and create tables
            db.create_all()
        except Exception as e:
            print(f"Database error: {e}")
            # If database schema is outdated, try to add missing columns
            try:
                # Check if we need to add missing columns to existing tables
                inspector = db.inspect(db.engine)

                # Check User table columns
                user_columns = [col['name'] for col in inspector.get_columns('user')]
                if 'reset_token' not in user_columns:
                    db.engine.execute("ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)")
                    print("Added reset_token column to user table")
                if 'reset_token_expiry' not in user_columns:
                    db.engine.execute("ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME")
                    print("Added reset_token_expiry column to user table")
                if 'admin_approved' not in user_columns:
                    db.engine.execute("ALTER TABLE user ADD COLUMN admin_approved BOOLEAN DEFAULT 0")
                    print("Added admin_approved column to user table")

                # Check Booking table columns
                booking_columns = [col['name'] for col in inspector.get_columns('booking')]
                if 'admin_approved' not in booking_columns:
                    db.engine.execute("ALTER TABLE booking ADD COLUMN admin_approved BOOLEAN DEFAULT 0")
                    print("Added admin_approved column to booking table")

                # Check Service table columns
                service_columns = [col['name'] for col in inspector.get_columns('service')]
                if 'service_group_id' not in service_columns:
                    db.engine.execute("ALTER TABLE service ADD COLUMN service_group_id INTEGER NOT NULL DEFAULT 1")
                    print("Added service_group_id column to service table")

                print("Database schema updated successfully!")
            except Exception as e2:
                print(f"Error updating database schema: {e2}")
                print("Please manually reset the database using: python force_db_reset.py")

    app.run(debug=True, host='127.0.0.1', port=5000)
