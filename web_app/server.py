import os
from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_session import Session
import argparse

from web_app.models import db, Camera, LicencePlate, ParkingHistory, LocationEntry
from sqlalchemy import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SECRET_KEY"
] = "GTHhNYGAhTDRTSYUDFVEsdf4wt3tWGU&GR$FGIU4reWUIGBWSEFGHIU*EWHFIUWE$GHUITW$EBUYFGHWE$HGWE$YU"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
db.init_app(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Serve login page and handle login POST request"""
    if request.method == "POST":
        data = request.get_json()
        plate = data.get("plate")

        licence_plate = LicencePlate.query.filter(func.lower(LicencePlate.plate) == func.lower(plate)).first()
        if not licence_plate:
            return jsonify({"error": "Licence plate not found"}), 404

        # Save the license plate in the session
        session["plate"] = plate

        # Return response
        return jsonify({"message": "Logged in", "error": False}), 200

    # Serve login.html for GET request
    return render_template("login.html")


@app.route("/")
def home():
    """Serve the home page"""
    plate = session.get("plate")
    if not plate:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/add_camera", methods=["POST"])
def add_camera():
    """Add camera POST function"""
    data = request.get_json()
    location = data.get("location")
    new_camera = Camera(location=location)
    db.session.add(new_camera)
    db.session.commit()
    return jsonify({"message": "Camera added", "location": location}), 201


@app.route("/enter_carpark", methods=["POST"])
def enter_carpark():
    """Register licence entering carpark POST function"""
    data = request.get_json()
    plate = data.get("plate")
    # Update or insert into licence_plates
    licence_plate = LicencePlate.query.get(plate)
    if licence_plate:
        licence_plate.last_seen = db.func.current_timestamp()
    else:
        licence_plate = LicencePlate(plate=plate)
        db.session.add(licence_plate)

    # Insert into parking_history
    parking_history = ParkingHistory(plate=plate)
    db.session.add(parking_history)

    db.session.commit()
    return jsonify({"message": "Car entered", "plate": plate}), 201


@app.route("/exit_carpark", methods=["POST"])
def exit_carpark():
    """Register licence exiting carpark POST function"""
    data = request.get_json()
    plate = data.get("plate")
    # Update licence_plates and parking_history
    licence_plate = LicencePlate.query.get(plate)
    if not licence_plate:
        return jsonify({"error": "Car not found"}), 404

    licence_plate.last_seen = db.func.current_timestamp()

    parking_history = (
        ParkingHistory.query.filter_by(plate=plate, exit_time=None)
        .order_by(ParkingHistory.entry_time.desc())
        .first()
    )
    if parking_history:
        parking_history.exit_time = db.func.current_timestamp()

    db.session.commit()
    return jsonify({"message": "Car exited", "plate": plate}), 201


@app.route("/add_location_entry", methods=["POST"])
def add_location_entry():
    """Register licence to a location POST function"""
    data = request.get_json()

    # Retrieve data from request
    plate = data.get("plate")
    camera_id = data.get("camera_id")

    # Check if camera_id exists
    camera = Camera.query.get(camera_id)
    if camera is None:
        return jsonify({"error": "Camera with provided ID does not exist"}), 400
    

    # Check if plate exists
    licence_plate = LicencePlate.query.get(plate)
    if licence_plate:
        licence_plate.last_seen = db.func.current_timestamp()
    else:
        licence_plate = LicencePlate(plate=plate)
        db.session.add(licence_plate)

    # Insert into parking_history
    parking_history = ParkingHistory(plate=plate)
    db.session.add(parking_history)

    # Create new LocationEntry
    location_entry = LocationEntry(plate=plate, camera_id=camera_id)
    db.session.add(location_entry)
    db.session.commit()

    print(f"Logged car plate:{plate} at camera:{camera_id}")

    return (
        jsonify(
            {"message": "Location entry added", "plate": plate, "camera_id": camera_id}
        ),
        201,
    )


# @app.route('/get_car_info/<plate>', methods=['GET'])
def get_car_info_by_plate(plate):
    """Get information about licence plate

    Args:
        plate (string): Licence plate

    """
    entry = (
        db.session.query(LocationEntry, Camera.location)
        .join(Camera)
        .filter(LocationEntry.plate.ilike(plate))
        .order_by(LocationEntry.timestamp.desc())
        .first()
    )
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    location_entry, location = entry
    return (
        jsonify(
            {
                "plate": location_entry.plate,
                "timestamp": location_entry.timestamp.isoformat(),
                "location": location,
            }
        ),
        200,
    )


@app.route("/get_car_info", methods=["GET"])
def get_car_info():
    plate = session.get("plate")
    if not plate:
        return jsonify({"error": "Not logged in"}), 401
    return get_car_info_by_plate(plate)


# Init the database if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask application")
    parser.add_argument("--debug", action="store_true", help="Run app in debug mode")

    args = parser.parse_args()

    app.run(host="0.0.0.0", debug=args.debug)
