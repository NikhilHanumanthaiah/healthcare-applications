"""
Migration script to add email column to patients table
Run this once to update the existing database schema
"""

from app.infrastructure.db.session import engine
from sqlalchemy import text


def add_email_column():
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(
            text(
                """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='patients' AND column_name='email'
        """
            )
        )

        if result.fetchone() is None:
            # Add the email column
            conn.execute(
                text(
                    """
                ALTER TABLE patients 
                ADD COLUMN email VARCHAR NULL
            """
                )
            )
            conn.commit()
            print("✅ Email column added successfully!")
        else:
            print("ℹ️  Email column already exists")


if __name__ == "__main__":
    add_email_column()
