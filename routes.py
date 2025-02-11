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


@routes.route('/scan/<string:badge_code>', methods=['POST'])
def add_scan(badge_code):
    # find the user by 'badge_code'
    user = User.query.filter_by(badge_code=badge_code).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get json data from request
    data = request.get_json()
    if not data or "activity_name" not in data or "activity_category" not in data:
        return jsonify({"error": "Missing activity_name or activity_category in request data"}), 400

    activity_name = data["activity_name"]
    activity_category = data["activity_category"]

    # if the acitivity exists if not then create it
    activity = Activity.query.filter_by(name=activity_name).first()
    if not activity:
        activity = Activity(name=activity_name, category=activity_category)
        db.session.add(activity)
        db.session.commit()  

    # create a new scan record
    new_scan = Scan(
        user_id=user.id,
        activity_id=activity.id,
        scanned_at=datetime.now(timezone.utc)
    )
    db.session.add(new_scan)

    # update the user's 'updated_at' field
    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    scan_data = {
        "activity_name": activity.name,
        "activity_category": activity.category,
        "scanned_at": new_scan.scanned_at.isoformat()
    }
    return jsonify(scan_data), 201


@routes.route('/scans', methods=['GET'])
def get_scan_data():
    
    min_frequency = request.args.get('min_frequency', type=int)
    max_frequency = request.args.get('max_frequency', type=int)
    activity_category = request.args.get('activity_category')

    query = db.session.query(
        Activity.name.label("activity_name"),
        db.func.count(Scan.id).label("frequency")
    ).join(Scan, Activity.id == Scan.activity_id).group_by(Activity.id)

    # apply filter for activity category if provided
    if activity_category:
        query = query.filter(Activity.category == activity_category)

    # apply having clauses for aggregated counts if provided
    if min_frequency is not None:
        query = query.having(db.func.count(Scan.id) >= min_frequency)
    if max_frequency is not None:
        query = query.having(db.func.count(Scan.id) <= max_frequency)

    results = query.all()

   
    scans_data = [
        {"activity_name": result.activity_name, "frequency": result.frequency}
        for result in results
    ]
    return jsonify(scans_data)
