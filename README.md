# Melon Reservation Scheduler

## Description
This project allows you to make and manage melon tasting reservations. 🍉

## Reflection
Given more time, I would incorporate a User table that would have a relationship with the Reservation table. With a User table, I could have a password field which would allow me to enable authentication. I would use the Python hashlib library with salt to encrypt the password. 

I would also like to add unit tests that test that a particular time does not show up in the list of available times when it's already booked. 

## Installation
To run Melon Reservation Schedule on your local machine:

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

Run the app:
```python3 server.py```

You can now navigate to 'localhost:5000/' to access Melon Tasting Scheduler.