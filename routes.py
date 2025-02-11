from flask import Blueprint, jsonify, request
from models import db, User, Scan, Activity
from datetime import datetime, timezone


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

@routes.route('/users/<string:badge_code>', methods=['GET'])
def get_user(badge_code):

    user = User.query.filter_by(badge_code=badge_code).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

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
    return jsonify(user_data)


@routes.route('/users/<string:badge_code>', methods=['PUT'])
def update_user(badge_code):

    user = User.query.filter_by(badge_code=badge_code).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        user.name = data["name"]
    if "phone" in data:
        user.phone = data["phone"]

    #updating the feild manually to be safe
    user.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating user", "details": str(e)}), 500

    # update data and reuturn it 
    updated_user_data = {
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
    return jsonify(updated_user_data)