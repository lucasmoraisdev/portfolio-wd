"""
Seed script to initialize database with default users
Usage: python -m app.scripts.seed
"""

from __future__ import annotations
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import select

from app.modules.user.models import User
from app.shared.database.session import SessionLocal
from app.shared.security.password import get_password_hash


def seed_database():
    """Add initial users to the database"""
    session = SessionLocal()
    
    try:
        # Check if admin user already exists
        stmt = select(User).where(User.email == "admin@example.com")
        existing_user = session.execute(stmt).scalar_one_or_none()
        
        if existing_user:
            print("Admin user already exists. Skipping seed.")
            return
        
        # Create admin user
        admin_user = User(
            name="Administrator",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        session.add(admin_user)
        session.commit()
        
        print("✓ Admin user created successfully!")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print("\nPlease change the password after first login!")
        
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
