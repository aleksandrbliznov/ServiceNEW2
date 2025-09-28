#!/usr/bin/env python3
"""
Fix commission records for existing bookings.
This script creates commission records for bookings that don't have them.
"""

from app import app, db, Commission, Booking, Service

def fix_commissions():
    """Create commission records for existing bookings that don't have them."""
    with app.app_context():
        try:
            # Get all bookings that don't have commission records
            bookings_without_commissions = []

            for booking in Booking.query.all():
                commission_exists = Commission.query.filter_by(booking_id=booking.id).first()
                if not commission_exists:
                    bookings_without_commissions.append(booking)

            print(f"Found {len(bookings_without_commissions)} bookings without commission records")

            # Create commission records for these bookings
            for booking in bookings_without_commissions:
                try:
                    # Skip bookings without assigned handyman (pending bookings)
                    if not booking.handyman_id:
                        print(f"Skipping booking {booking.id}: No handyman assigned (status: {booking.status})")
                        continue

                    # Calculate commission
                    commission_amount = booking.total_price * 0.10  # 10% commission
                    handyman_earnings = booking.total_price * 0.90  # 90% to handyman

                    commission = Commission(
                        booking_id=booking.id,
                        handyman_id=booking.handyman_id,
                        service_price=booking.total_price,
                        commission_amount=commission_amount,
                        handyman_earnings=handyman_earnings
                    )

                    db.session.add(commission)
                    print(f"Created commission for booking {booking.id}: ${commission_amount} commission, ${handyman_earnings} earnings")

                except Exception as e:
                    print(f"Error creating commission for booking {booking.id}: {e}")

            # Commit all changes
            db.session.commit()
            print(f"Successfully created {len(bookings_without_commissions)} commission records")

            # Show final statistics
            total_commissions = Commission.query.count()
            total_commission_amount = sum(c.commission_amount for c in Commission.query.all())
            total_handyman_earnings = sum(c.handyman_earnings for c in Commission.query.all())

            print("\nCommission Statistics:")
            print(f"Total commission records: {total_commissions}")
            print(f"Total commission amount: ${total_commission_amount:.2f}")
            print(f"Total handyman earnings: ${total_handyman_earnings:.2f}")

        except Exception as e:
            print(f"Error fixing commissions: {e}")
            db.session.rollback()

if __name__ == '__main__':
    fix_commissions()