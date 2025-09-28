#!/usr/bin/env python3
from app import app, db, User, Service

with app.app_context():
    print('Checking database...')
    print(f'Users: {User.query.count()}')
    print(f'Services: {Service.query.count()}')

    admin = User.query.filter_by(username='admin').first()
    print(f'Admin exists: {admin is not None}')
    if admin:
        print(f'Admin role: {admin.role}')
        print(f'Admin email: {admin.email}')
        print(f'Admin approved: {admin.is_approved}')

    # Check services
    services = Service.query.filter_by(is_active=True).all()
    print(f'Active services: {len(services)}')
    for service in services:
        print(f'  - {service.name}: ${service.price}')