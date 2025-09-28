"""
REST API for Service PRO Frontend
Provides JSON endpoints for the React frontend
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime
import json

# Import models to avoid circular import
def get_models():
    from app import db, User, Service, ServiceGroup, Booking, Feedback, Commission
    return db, User, Service, ServiceGroup, Booking, Feedback, Commission

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# User roles
USER = 'user'
ADMIN = 'admin'
HANDYMAN = 'handyman'

@api_bp.route('/service-groups')
def get_service_groups():
    """Get all active service groups"""
    try:
        db, User, Service, ServiceGroup, Booking, Feedback, Commission = get_models()
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

@api_bp.route('/services')
@login_required
def get_services():
    """Get services, optionally filtered by group"""
    try:
        db, User, Service, ServiceGroup, Booking, Feedback, Commission = get_models()
        group_id = request.args.get('group_id', type=int)
        user_role = current_user.role

        query = Service.query.filter_by(is_active=True, is_approved=True)

        if group_id:
            query = query.filter_by(service_group_id=group_id)

        # Different filtering based on user role
        if user_role == USER:
            # Customers see all approved services
            pass
        elif user_role == HANDYMAN:
            # Handymen see all approved services plus their own pending ones
            query = query.filter(
                db.or_(
                    Service.is_approved == True,
                    Service.handyman_id == current_user.id
                )
            )
        elif user_role == ADMIN:
            # Admins see all services
            pass

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

@api_bp.route('/services/<int:service_id>')
def get_service(service_id):
    """Get a specific service"""
    try:
        service = Service.query.get_or_404(service_id)
        return jsonify({
            'success': True,
            'data': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': float(service.price),
                'duration_hours': service.duration_hours,
                'category': service.category,
                'service_group_id': service.service_group_id,
                'handyman_id': service.handyman_id,
                'is_active': service.is_active,
                'is_approved': service.is_approved,
                'example_images': json.loads(service.example_images) if service.example_images else [],
                'created_at': service.created_at.isoformat() if service.created_at else None,
                'updated_at': service.updated_at.isoformat() if service.updated_at else None,
                'service_group': {
                    'id': service.service_group.id,
                    'name': service.service_group.name,
                    'name_et': service.service_group.name_et,
                    'name_en': service.service_group.name_en,
                    'name_ru': service.service_group.name_ru,
                    'description': service.service_group.description
                } if service.service_group else None,
                'handyman': {
                    'id': service.handyman.id,
                    'first_name': service.handyman.first_name,
                    'last_name': service.handyman.last_name,
                    'phone': service.handyman.phone,
                    'average_score': float(service.handyman.average_score) if service.handyman.average_score else 0,
                    'total_feedbacks': service.handyman.total_feedbacks
                } if service.handyman else None
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/bookings', methods=['GET', 'POST'])
@login_required
def handle_bookings():
    """Get user bookings or create new booking"""
    if request.method == 'GET':
        # Get user's bookings
        try:
            bookings = Booking.query.filter_by(user_id=current_user.id).all()
            return jsonify({
                'success': True,
                'data': [{
                    'id': b.id,
                    'service_id': b.service_id,
                    'handyman_id': b.handyman_id,
                    'booking_date': b.booking_date.isoformat() if b.booking_date else None,
                    'status': b.status,
                    'special_requests': b.special_requests,
                    'total_price': float(b.total_price),
                    'admin_approved': b.admin_approved,
                    'created_at': b.created_at.isoformat() if b.created_at else None,
                    'service': {
                        'id': b.service.id,
                        'name': b.service.name,
                        'price': float(b.service.price)
                    } if b.service else None,
                    'handyman': {
                        'id': b.handyman.id,
                        'first_name': b.handyman.first_name,
                        'last_name': b.handyman.last_name
                    } if b.handyman else None
                } for b in bookings]
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    elif request.method == 'POST':
        # Create new booking
        try:
            data = request.get_json()
            service_id = data.get('service_id')
            booking_date = data.get('booking_date')
            special_requests = data.get('special_requests', '')

            if not service_id or not booking_date:
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400

            service = Service.query.get_or_404(service_id)

            # Verify service is approved and active
            if not service.is_approved or not service.is_active:
                return jsonify({'success': False, 'error': 'Service is not available for booking'}), 400

            # Parse booking date
            try:
                booking_date = datetime.fromisoformat(booking_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid date format'}), 400

            # Validate that booking date is in the future
            if booking_date <= datetime.now():
                return jsonify({'success': False, 'error': 'Please select a future date and time'}), 400

            booking = Booking(
                user_id=current_user.id,
                service_id=service_id,
                booking_date=booking_date,
                special_requests=special_requests,
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

            return jsonify({
                'success': True,
                'message': 'Booking created successfully',
                'data': {
                    'id': booking.id,
                    'total_price': float(booking.total_price),
                    'status': booking.status
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    """Get user dashboard data"""
    if current_user.role != USER:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': current_user.id,
                    'first_name': current_user.first_name,
                    'last_name': current_user.last_name
                },
                'bookings': [{
                    'id': b.id,
                    'service_name': b.service.name if b.service else 'Unknown Service',
                    'handyman_name': f"{b.handyman.first_name} {b.handyman.last_name}" if b.handyman else 'Unassigned',
                    'booking_date': b.booking_date.isoformat() if b.booking_date else None,
                    'status': b.status,
                    'total_price': float(b.total_price)
                } for b in bookings]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/handyman/dashboard')
@login_required
def handyman_dashboard():
    """Get handyman dashboard data"""
    if current_user.role != HANDYMAN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        bookings = Booking.query.filter_by(handyman_id=current_user.id).all()
        services = Service.query.filter_by(handyman_id=current_user.id).all()

        return jsonify({
            'success': True,
            'data': {
                'handyman': {
                    'id': current_user.id,
                    'first_name': current_user.first_name,
                    'last_name': current_user.last_name,
                    'average_score': float(current_user.average_score) if current_user.average_score else 0,
                    'total_feedbacks': current_user.total_feedbacks
                },
                'bookings': [{
                    'id': b.id,
                    'service_name': b.service.name if b.service else 'Unknown Service',
                    'customer_name': f"{b.user.first_name} {b.user.last_name}" if b.user else 'Unknown Customer',
                    'booking_date': b.booking_date.isoformat() if b.booking_date else None,
                    'status': b.status,
                    'total_price': float(b.total_price)
                } for b in bookings],
                'services': [{
                    'id': s.id,
                    'name': s.name,
                    'is_approved': s.is_approved,
                    'is_active': s.is_active
                } for s in services]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Get admin dashboard data"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        total_users = User.query.count()
        total_services = Service.query.filter_by(is_approved=True).count()
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        pending_handymen = User.query.filter_by(role=HANDYMAN, is_approved=False).count()
        pending_services_count = Service.query.filter_by(is_approved=False).count()
        total_service_groups = ServiceGroup.query.filter_by(is_active=True).count()

        # Get handyman statistics
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

        return jsonify({
            'success': True,
            'data': {
                'stats': {
                    'total_users': total_users,
                    'total_services': total_services,
                    'total_bookings': total_bookings,
                    'pending_bookings': pending_bookings,
                    'pending_handymen': pending_handymen,
                    'pending_services_count': pending_services_count,
                    'total_service_groups': total_service_groups,
                    'total_earnings': float(total_earnings),
                    'in_progress_jobs': in_progress_jobs,
                    'completed_jobs': completed_jobs,
                    'approved_handymen_count': len(approved_handymen),
                    'total_commission_amount': float(total_commission_amount),
                    'total_handyman_earnings': float(total_handyman_earnings)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/auth/me')
@login_required
def get_current_user():
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

@api_bp.route('/admin/approve-service/<int:service_id>', methods=['POST'])
@login_required
def api_admin_approve_service(service_id):
    """API endpoint to approve a service (admin only)"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        service = Service.query.get_or_404(service_id)
        service.is_approved = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Service "{service.name}" has been approved successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/reject-service/<int:service_id>', methods=['DELETE'])
@login_required
def api_admin_reject_service(service_id):
    """API endpoint to reject and delete a service (admin only)"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        service = Service.query.get_or_404(service_id)
        service_name = service.name
        db.session.delete(service)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Service "{service_name}" has been rejected and deleted'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/pending-services')
@login_required
def api_admin_pending_services():
    """Get all pending services for admin approval"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        pending_services = Service.query.filter_by(is_approved=False).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'price': float(s.price),
                'duration_hours': s.duration_hours,
                'category': s.category,
                'service_group': {
                    'id': s.service_group.id,
                    'name': s.service_group.name
                } if s.service_group else None,
                'handyman': {
                    'id': s.handyman.id,
                    'first_name': s.handyman.first_name,
                    'last_name': s.handyman.last_name,
                    'email': s.handyman.email
                } if s.handyman else None,
                'created_at': s.created_at.isoformat() if s.created_at else None
            } for s in pending_services]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/approve-service/<int:service_id>', methods=['POST'])
@login_required
def api_approve_service(service_id):
    """API endpoint to approve a service (admin only)"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        db, User, Service, ServiceGroup, Booking, Feedback, Commission = get_models()
        service = Service.query.get_or_404(service_id)
        service.is_approved = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Service "{service.name}" has been approved successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/reject-service/<int:service_id>', methods=['DELETE'])
@login_required
def api_reject_service(service_id):
    """API endpoint to reject and delete a service (admin only)"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        db, User, Service, ServiceGroup, Booking, Feedback, Commission = get_models()
        service = Service.query.get_or_404(service_id)
        service_name = service.name
        db.session.delete(service)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Service "{service_name}" has been rejected and deleted'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/admin/pending-services')
@login_required
def api_get_pending_services():
    """Get all pending services for admin approval"""
    if current_user.role != ADMIN:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    try:
        db, User, Service, ServiceGroup, Booking, Feedback, Commission = get_models()
        pending_services = Service.query.filter_by(is_approved=False).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'price': float(s.price),
                'duration_hours': s.duration_hours,
                'category': s.category,
                'service_group': {
                    'id': s.service_group.id,
                    'name': s.service_group.name
                } if s.service_group else None,
                'handyman': {
                    'id': s.handyman.id,
                    'first_name': s.handyman.first_name,
                    'last_name': s.handyman.last_name,
                    'email': s.handyman.email
                } if s.handyman else None,
                'created_at': s.created_at.isoformat() if s.created_at else None
            } for s in pending_services]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Register API blueprint
def init_api(app):
    """Initialize API blueprint"""
    app.register_blueprint(api_bp)