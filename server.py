from flask import Flask, render_template, request, flash, session, redirect, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import db, connect_to_db, Reservation
import pytz
import os

app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET_KEY"]
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
    reservation_start = parse(request.form.get("startTime"))
    username = session["username"]
    reservation_to_delete = Reservation.query\
        .filter(Reservation.start_time==reservation_start)\
        .filter(Reservation.username==username)\
        .first()
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return jsonify(reservation_to_delete.reservation_id)

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    reservation_start = parse(request.form.get("start_time"))
    username = session["username"]

    new_reservaton = Reservation(username=username, start_time=reservation_start)
    db.session.add(new_reservaton)
    db.session.commit()
    return redirect("/reservations")

@app.route("/search_reservations", methods=["POST"])
def search_reservation():
    start_time = parse(request.form.get("startTime"))
    end_time = parse(request.form.get("endTime"))

    # retrieve reservations in within the specified time range 
    all_reservations_in_range = (
        db.session.query(Reservation.start_time)\
        .filter(Reservation.start_time.between(start_time, end_time))\
    )
    # get reservation times without time zone
    existing_reservation_times = \
        {res[0].replace(tzinfo=None) for res in all_reservations_in_range.all()}

    # of exisitng reservations, get the ones with the user
    user_reservations = all_reservations_in_range\
        .filter(Reservation.username==session["username"])\
        .all()
    user_reservation_dates = {res.start_time.date()for res in user_reservations}

    # Initialize list for possible times 
    times = []
   
    # Possible reservations can only happen on the half hour
    first_reservation_time = start_time + (datetime.min - start_time) \
        % timedelta(minutes=30)
    current = first_reservation_time

    # Add possible times, filtering where a reservation already exists OR where
    # user already has a reservation on that date
    while current < end_time:
        if current not in existing_reservation_times and current.date() not in user_reservation_dates:
            times.append(current)
        current = current + timedelta(minutes=30)
    return jsonify(times)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)