#!/usr/bin/env python3
"""
Create a working database for Service PRO
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def create_database():
    """Create a working SQLite database"""
    db_path = 'service_app.db'

    # Remove existing file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    # Create new database
    conn = sqlite3.connect(db_path)
    print(f"Created new database: {db_path}")

    # Create tables
    conn.execute('''
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        address TEXT,
        is_approved INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        reset_token TEXT UNIQUE,
        reset_token_expiry TEXT,
        average_score REAL DEFAULT 0.0,
        total_feedbacks INTEGER DEFAULT 0,
        admin_approved INTEGER DEFAULT 0
    )
    ''')

    conn.execute('''
    CREATE TABLE service (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        duration_hours INTEGER NOT NULL,
        category TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.execute('''
    CREATE TABLE booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        handyman_id INTEGER,
        booking_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        special_requests TEXT,
        total_price REAL NOT NULL,
        admin_approved INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.execute('''
    CREATE TABLE feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        handyman_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    print("Created all tables")

    # Insert admin user
    admin_password_hash = generate_password_hash('admin123')
    conn.execute('''
    INSERT INTO user (username, email, password_hash, role, first_name, last_name, is_approved)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', admin_password_hash, 'admin', 'Admin', 'User', 1))

    print("Inserted admin user")

    # Insert sample services
    services = [
        ('Plumbing Repair', 'Professional plumbing repair services', 75.0, 2, 'Plumbing'),
        ('Electrical Work', 'Electrical installation and repair', 85.0, 3, 'Electrical'),
        ('House Cleaning', 'Complete house cleaning service', 120.0, 4, 'Cleaning'),
        ('Garden Maintenance', 'Garden maintenance and landscaping', 60.0, 2, 'Gardening'),
        ('Painting', 'Interior and exterior painting', 200.0, 6, 'Painting'),
        ('Carpentry', 'Custom carpentry and woodwork', 90.0, 4, 'Carpentry')
    ]

    for service in services:
        conn.execute('''
        INSERT INTO service (name, description, price, duration_hours, category)
        VALUES (?, ?, ?, ?, ?)
        ''', service)
        print(f"Inserted service: {service[0]}")

    conn.commit()
    conn.close()

    # Verify the database
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables created: {[table[0] for table in tables]}")

    cursor = conn.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    print(f"Users in database: {user_count}")

    cursor = conn.execute("SELECT COUNT(*) FROM service")
    service_count = cursor.fetchone()[0]
    print(f"Services in database: {service_count}")

    conn.close()

    print("Database created successfully!")

    return True

if __name__ == '__main__':
    create_database()