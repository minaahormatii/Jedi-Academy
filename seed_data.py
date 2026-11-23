
from flask_bcrypt import generate_password_hash

from app import app
from db import db
from models.temple import Temples
from models.app_user import AppUsers


with app.app_context():
    existing_user = (
        db.session.query(AppUsers)
        .filter(AppUsers.role == "grand-master")
        .first()
    )

    if existing_user:
        print("A Grand Master already exists.")
    else:
        temple = Temples(
            "Jedi Temple",
            "Coruscant",
            0,
            10,
            True,
        )

        db.session.add(temple)
        db.session.flush()

        password_hash = generate_password_hash("JediMaster123!")

        if isinstance(password_hash, bytes):
            password_hash = password_hash.decode("utf-8")

        grand_master = AppUsers(
            temple.temple_id,
            "grandmaster",
            "master@example.com",
            password_hash,
            "grand-master",
            0,
            True,
        )

        db.session.add(grand_master)
        db.session.commit()

        print("Initial Temple and Grand Master created!")
        print("Email: master@example.com")
        print("Password: JediMaster123!")
