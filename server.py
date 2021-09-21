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
    username = request.form.get("username")
    existing_reservations = Reservation.query.filter_by(username=username).all()
    return render_template("reservations.html", reservations=existing_reservations)

@app.route("/schedule")
def render_schedule():
    return render_template("schedule.html")

@app.route("/api/reservations/<reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    reservation_to_delete = Reservation.query.get(reservation_id)
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return jsonify(f"Reservation {reservation_id} deleted")

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    print("**************************************")
    print(request.form.get("start_time"))
    reservation_start = parse(request.form.get("start_time"))
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
    # print("***************************************")
    # print(type(start_time))
    # first_reservation_time = start_time + (
    #     datetime.min.replace(tzinfo=pytz.UTC) - start_time
    # ) % timedelta(minutes=30)
    current = start_time#first_reservation_time
    times = []

    all_reservations_in_range = (
        db.session.query(Reservation.start_time)
        .filter(Reservation.start_time.between(start_time, end_time))
        .all()
    )
    # ADD THE FILTERING - REMOVE THE ONES THAT ALREADY EXIST
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