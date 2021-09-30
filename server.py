from flask import Flask, render_template, request, flash, session, redirect, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import db, connect_to_db, available_reservations, \
    retrieve_reservations, create_reservation, delete_reservations
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
    """ Retrieve reservations the user has made."""
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
    else:
        # if the user is not in session, redirect them to the homepage
        if 'username' in session:
            username = session["username"]
        else:
            redirect("/")
    existing_reservations = retrieve_reservations(username)

    return render_template("reservations.html", reservations=existing_reservations)

@app.route("/schedule")
def render_schedule():
    """ View scheduling page."""
    return render_template("schedule.html")

@app.route("/reservations/delete", methods=["POST"])
def delete_reservation():
    """ Delete reservations the user has made."""
    reservation_start = parse(request.form.get("startTime"))
    username = session["username"]

    reservation_to_delete = delete_reservations(reservation_start, username)
    return jsonify(reservation_to_delete.reservation_id)

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    """ Create a reserviation with the specified user and time."""
    reservation_start = parse(request.form.get("start_time"))
    username = session["username"]

    create_reservation(username, reservation_start)
    return redirect("/reservations")

@app.route("/search_reservations", methods=["GET"])
def search_reservation():
    start_time = parse(request.args.get("startTime"))
    end_time = parse(request.args.get("endTime"))

    available_times = available_reservations(start_time, end_time, session["username"])
    return jsonify(available_times)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)