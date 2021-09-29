Melon Reservation Scheduler

This project allows you to make and manage melon tasting reservations. 🍉

Installation
To run Melon Reservation Schedule on your local machine:

Clone this repo:

https://github.com/sorbetlemon16/melon_takehome.git
Create and activate a virtual environment inside your projec directory:

virtualenv env (Mac OS)
virtualenv env --always-copy (Windows OS)
source env/bin/activate
Install the dependencies:

pip3 install -r requirements.txt
Set up the database:

python3 seed.py
Run the app:

python3 server.py
You can now navigate to 'localhost:5000/' to access Melon Tasting Scheduler.