from app import app, db

with app.app_context():
    db.drop_all()      # Removes old tables if any
    db.create_all()    # Creates new tables
    print("Database created successfully!")