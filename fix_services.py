#!/usr/bin/env python3
"""
Script to fix service issues in the database
"""

from app import app, db, Service, ServiceGroup

def fix_services():
    """Fix pending services and incorrect group assignments"""
    with app.app_context():
        print("Starting service fixes...")

        # Approve all pending services
        pending_services = Service.query.filter_by(is_approved=False).all()
        print(f"Found {len(pending_services)} pending services")

        for service in pending_services:
            service.is_approved = True
            print(f"Approved service: {service.name}")

        # Fix incorrect service group assignments
        print("\nFixing service group assignments...")

        # Lawn Mowing -> Gardening
        lawn_mowing = Service.query.filter_by(name='Lawn Mowing').first()
        if lawn_mowing:
            gardening_group = ServiceGroup.query.filter_by(name='Gardening').first()
            if gardening_group:
                old_group = ServiceGroup.query.get(lawn_mowing.service_group_id)
                lawn_mowing.service_group_id = gardening_group.id
                print(f"Fixed Lawn Mowing: {old_group.name if old_group else 'Unknown'} -> {gardening_group.name}")

        # Painting Service -> Construction
        painting = Service.query.filter_by(name='Painting Service').first()
        if painting:
            construction_group = ServiceGroup.query.filter_by(name='Construction').first()
            if construction_group:
                old_group = ServiceGroup.query.get(painting.service_group_id)
                painting.service_group_id = construction_group.id
                print(f"Fixed Painting Service: {old_group.name if old_group else 'Unknown'} -> {construction_group.name}")

        # HVAC Maintenance -> Construction
        hvac = Service.query.filter_by(name='HVAC Maintenance').first()
        if hvac:
            construction_group = ServiceGroup.query.filter_by(name='Construction').first()
            if construction_group:
                old_group = ServiceGroup.query.get(hvac.service_group_id)
                hvac.service_group_id = construction_group.id
                print(f"Fixed HVAC Maintenance: {old_group.name if old_group else 'Unknown'} -> {construction_group.name}")

        # Commit all changes
        db.session.commit()
        print("\nAll changes committed successfully!")

        # Show final state
        print("\nFinal service status:")
        all_services = Service.query.filter_by(is_active=True).all()
        for service in all_services:
            group = ServiceGroup.query.get(service.service_group_id)
            print(f"  {service.name} -> {group.name if group else 'No Group'} (Approved: {service.is_approved})")

if __name__ == '__main__':
    fix_services()