from flask import Blueprint, jsonify
from models import db, User, Scan, Activity

routes = Blueprint("routes", __name__)

@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    
    user_list = []
    for user in users:
        user_data = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "badge_code": user.badge_code,
            "updated_at": user.updated_at.isoformat(),
            "scans": [
                {
                    "activity_name": scan.activity.name,
                    "activity_category": scan.activity.category,
                    "scanned_at": scan.scanned_at.isoformat()
                }
                for scan in user.scans
            ]
        }
        user_list.append(user_data)

    return jsonify(user_list)
