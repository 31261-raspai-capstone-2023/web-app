from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LicencePlate(db.Model):
    __tablename__ = "licence_plates"
    plate = db.Column(db.String(255), primary_key=True)
    first_seen = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_seen = db.Column(db.DateTime, default=db.func.current_timestamp())
    parking_histories = db.relationship("ParkingHistory", backref="licence_plate")
    location_entries = db.relationship("LocationEntry", backref="licence_plate")


class ParkingHistory(db.Model):
    __tablename__ = "parking_history"
    plate = db.Column(
        db.String(255), db.ForeignKey("licence_plates.plate"), primary_key=True
    )
    entry_time = db.Column(
        db.DateTime, default=db.func.current_timestamp(), primary_key=True
    )
    exit_time = db.Column(db.DateTime)


class Camera(db.Model):
    __tablename__ = "cameras"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255), nullable=False)
    location_entries = db.relationship("LocationEntry", backref="camera")


class LocationEntry(db.Model):
    __tablename__ = "location_entries"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(
        db.String(255), db.ForeignKey("licence_plates.plate"), nullable=False
    )
    camera_id = db.Column(db.Integer, db.ForeignKey("cameras.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
