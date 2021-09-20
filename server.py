from flask import Flask, jsonify, request
from sqlalchemy import func
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import db, connect_to_db, Reservation
import pytz
import os

app = Flask(__name__, static_folder="./build", static_url_path="/")
app.secret_key = os.environ["APP_SECRET_KEY"]
local_dev = os.environ.get("ENV", "") == "development"
db_uri = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
connect_to_db(app, db_uri, echo=local_dev)


@app.route("/api/user/<username>/reservations/", methods=["GET"])
def get_user_reservations(username):
    existing_reservations_for_user = Reservation.query.filter_by(
        username=username
    ).all()
    return jsonify([res.to_dict() for res in existing_reservations_for_user])


@app.route("/api/reservations/<reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    reservation_to_delete = Reservation.query.get(reservation_id)
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return jsonify(f"Reservation {reservation_id} deleted")


@app.route("/api/reservations/book", methods=["POST"])
def make_reservation():
    reservation_start = parse(request.get_json()["startTime"])
    username = request.get_json()["username"]
    try:
        existing_reservations_for_user = (
            Reservation.query.filter(
                func.date(Reservation.start_time) == reservation_start.date()
            )
            .filter_by(username=username)
            .all()
        )
        if len(existing_reservations_for_user) > 0:
            return jsonify(
                {
                    "success": False,
                    "error": "User already has a reservation on this day",
                }
            )
        new_reservaton = Reservation(username=username, start_time=reservation_start)
        db.session.add(new_reservaton)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": e})


@app.route("/api/reservations", methods=["POST"])
def search_reservation():
    start_time = parse(request.get_json()["startTime"])
    end_time = parse(request.get_json()["endTime"])
    first_reservation_time = start_time + (
        datetime.min.replace(tzinfo=pytz.UTC) - start_time
    ) % timedelta(minutes=30)
    current = first_reservation_time
    times = []

    all_reservations_in_range = (
        db.session.query(Reservation.start_time)
        .filter(Reservation.start_time.between(start_time, end_time))
        .all()
    )
    existing_reservation_times = {res[0] for res in all_reservations_in_range}
    while current < end_time:
        if current not in existing_reservation_times:
            times.append(current.isoformat())
        current = current + timedelta(minutes=30)
    return jsonify(times)


# production site
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return app.send_static_file("index.html")

@app.errorhandler(404)
def not_found(_error):
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)