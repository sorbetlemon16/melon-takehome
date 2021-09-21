import os

import model
import server

os.system("dropdb reservations")
os.system("createdb reservations")

model.connect_to_db(server.app)
model.db.create_all()