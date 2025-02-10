import json
from datetime import datetime
from app import app, db
from models import User, Activity, Scan

#Loading json data from example file
with open("example_data.json", "r") as file:
    data = json.load(file)

# importing data into the database
def import_users():
    with app.app_context():
        for user_data in data:
            #make sure the badge_code is not empty if so skip the user
            if not user_data["badge_code"].strip():
                print(f"Skipping user {user_data['name']} (missing badge_code)")
                continue 

            # to avoid duplicates check if a user already exists
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if not existing_user:
                # if not then we will create new user entry
                new_user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    phone=user_data["phone"],
                    badge_code=user_data["badge_code"],
                    updated_at=datetime.utcnow()
                )
                db.session.add(new_user)
                db.session.commit()

                # Add user's scans
                for scan in user_data["scans"]:
                    # Check if activity exists, if not then create it
                    activity = Activity.query.filter_by(name=scan["activity_name"]).first()
                    if not activity:
                        activity = Activity(
                            name=scan["activity_name"],
                            category=scan["activity_category"]
                        )
                        db.session.add(activity)
                        db.session.commit()

                    # Create scan record
                    new_scan = Scan(
                        user_id=new_user.id,
                        activity_id=activity.id,
                        scanned_at=datetime.fromisoformat(scan["scanned_at"])
                    )
                    db.session.add(new_scan)

                db.session.commit() 

        print("Data import complete!")

# Run the import function
if __name__ == "__main__":
    import_users()