import os

from app import create_app, db

app = create_app()

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
