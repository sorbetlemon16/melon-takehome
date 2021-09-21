from flask import Flask, render_template, request, flash, session, redirect, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import db, connect_to_db, Reservation
import pytz
import os

app = Flask(__name__)
app.secret_key = "fake secret key"
# os.environ["APP_SECRET_KEY"]
# local_dev = os.environ.get("ENV", "") == "development"
# db_uri = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
connect_to_db(app)

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("index.html")

@app.route("/reservations", methods=["POST", "GET"])
def get_user_reservations():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
    else:
        username = session["username"]
    existing_reservations = Reservation.query.filter_by(username=username).all()
    return render_template("reservations.html", reservations=existing_reservations)

@app.route("/schedule")
def render_schedule():
    return render_template("schedule.html")

@app.route("/reservations/delete", methods=["POST"])
def delete_reservation():
    print("*********************")
    print(request.form.get("startTime"))
    reservation_start = parse(request.form.get("startTime"))
    print(request.form.get("startTime"))
    username = session["username"]
    reservation_to_delete = Reservation.query.filter(Reservation.start_time==reservation_start).filter(Reservation.username==username).first()
    print("*********************")
    print(reservation_to_delete)
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return jsonify(reservation_to_delete.reservation_id)

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    reservation_start = parse(request.form.get("start_time"))
    username = session["username"]

    # username = request.get_json()["username"]
    existing_reservations_for_user = (
        Reservation.query.filter(
            func.date(Reservation.start_time) == reservation_start.date()
        )
        .filter_by(username=username)
        .all()
    )
    # if len(existing_reservations_for_user) > 0:
    #     return jsonify(
    #         {
    #             "success": False,
    #             "error": "User already has a reservation on this day",
    #         }
    #     )
    new_reservaton = Reservation(username=username, start_time=reservation_start)
    db.session.add(new_reservaton)
    db.session.commit()
    return redirect("/reservations")

@app.route("/api/reservations", methods=["POST"])
def search_reservation():
    #start_time = parse(request.get_json()["startTime"])
    start_time = parse(request.form.get("startTime"))
    #end_time = parse(request.get_json()["endTime"])
    end_time = parse(request.form.get("endTime"))

    # possible reservations can only happen on the half hour
    first_reservation_time = start_time + (datetime.min - start_time) \
        % timedelta(minutes=30)
    current = first_reservation_time
    times = []

    all_reservations_in_range = (
        db.session.query(Reservation.start_time)
        .filter(Reservation.start_time.between(start_time, end_time))
        .all()
    )
    # Add possible times, filtering where a reservation already exists
    existing_reservation_times = {res[0] for res in all_reservations_in_range}
    while current < end_time:
        if current not in existing_reservation_times:
            times.append(current)
        current = current + timedelta(minutes=30)
    return jsonify(times)


# production site
# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
# def index(path):
#     return app.send_static_file("templates/index.html")

# @app.errorhandler(404)
# def not_found(_error):
#     return app.send_static_file("templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)