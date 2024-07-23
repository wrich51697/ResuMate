import os
from app import create_app, db_manager  # Import db_manager instead of db

app = create_app()

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db_manager.get_db().create_all()  # Use db_manager to create the tables
        print("Database tables created successfully.")
    app.run(debug=True)
