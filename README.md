# Melon Reservation Scheduler

## Description
This project allows you to make and manage melon tasting reservations. 🍉

## Justification
I chose to use Flask because it is a lightweight web framework that is flexible and simple to implement. I used postgreSQL because it's a commonly used relational database and makes a good choice since every reservation has a consistent format. SQLAlchemy allowed me to incorporate these two technologies using Python. I used Jinja to programmatically generate HTML and AJAX to handle retrieving available reservations from the database so that the page does not need to reload after the user submits their query.     

## Reflection
In addition to fulfilling the requirements, I also added delete functionality which also includes an AJAX request so when users delete reservations they will immediately be removed from the page. I also ensured that my web app is responsive to different screen sizes.

Given more time, I would incorporate a User table that would have a relationship with the Reservation table. With a User table, I could have a password field which would allow me to enable authentication. I would use the Python hashlib library with salt to encrypt the password. 

I would also like to add unit tests that test that a particular time does not show up in the list of available times when it's already booked. I added error handling for if a user goes to the /reservations URL if the user is not in session, which could occur with other routes as well. However, since the user is unable to navigate to these routes without being in session (unless they manually enter the URL) I did not include error handling there. 

## Installation
To run Melon Reservation Schedule on your local machine, follow the instructions below (note: these instructions assume you have Postgres installed and running):

Clone this repo: https://github.com/sorbetlemon16/melon_takehome.git

Create and activate a virtual environment inside your project directory:

```
virtualenv env (Mac OS)
virtualenv env --always-copy (Windows OS)
source env/bin/activate
```

Install the dependencies:
```pip3 install -r requirements.txt```

(Optionally) Seed the database:
```python3 seed.py```
Note: if you do not run ```seed.py```, make sure you create a database named
reservations: 
```createdb reservations```. 

Create a secrets.sh file to assign a value to APP_SECRET_KEY and run it:
```source secrets.sh```

Run the app:
```python3 server.py```

You can now navigate to 'localhost:5000/' to access Melon Tasting Scheduler.