#!/usr/bin/env python3
"""
Simple database connectivity test
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'check_same_thread': False}
}

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Try to connect
        result = db.engine.execute("SELECT 1")
        print("SQLAlchemy connection successful!")

        # Try to query users
        users = db.engine.execute("SELECT COUNT(*) FROM user").fetchone()
        print(f"Users found: {users[0]}")

        # Try to query services
        services = db.engine.execute("SELECT COUNT(*) FROM service").fetchone()
        print(f"Services found: {services[0]}")

        print("Database connectivity test PASSED!")

except Exception as e:
    print(f"Database connectivity test FAILED: {e}")
    print("This is a SQLAlchemy configuration issue.")