from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import routes


app = Flask(__name__)

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# register routes
app.register_blueprint(routes)

@app.route('/')
def home():
    return "Hackathon Badge Scanner API is running!"

if __name__ == '__main__':
    with app.app_context():
        # Create tables in database
        db.create_all()  
    app.run(debug=True)
