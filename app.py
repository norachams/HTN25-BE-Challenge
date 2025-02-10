from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return "Hackathon Badge Scanner API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in database
    app.run(debug=True)
