from app import app
from models import db, User

with app.app_context():

    db.create_all()

    admin = User(username="admin", password="admin", role="admin")

    cs = User(username="cs_hod", password="123", role="hod", subject="CS")

    civil = User(username="civil_hod", password="123", role="hod", subject="Civil")

    db.session.add(admin)
    db.session.add(cs)
    db.session.add(civil)

    db.session.commit()

print("Users Created Successfully")