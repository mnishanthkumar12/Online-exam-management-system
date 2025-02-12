from one import app, db
from one import User
from flask_bcrypt import Bcrypt
from datetime import datetime

# Initialize Bcrypt
bcrypt = Bcrypt()

def create_admin_user():
    with app.app_context():
        try:
            # Check if an admin user already exists
            if not User.query.filter_by(is_admin=True).first():
                # Create a new admin user
                hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
                # Ensure 'role' is provided here
                admin = User(username='admin', email='admin@example.com', role='admin', created_at=datetime.now(), password=hashed_password, is_admin=True)
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully.")
            else:
                print("Admin user already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_admin_user()
