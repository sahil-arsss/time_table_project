from app import app
from models import db, User

with app.app_context():

    db.create_all()

    # Admin
    admin = User(username="admin", password="admin", role="admin")

    # HOD Users
    cs = User(username="cs_hod", password="123", role="hod", subject="CS")

    civil = User(username="civil_hod", password="123", role="hod", subject="Civil")

    it = User(username="it_hod", password="123", role="hod", subject="IT")

    ece = User(username="ece_hod", password="123", role="hod", subject="ECE")

    electrical = User(username="electrical_hod", password="123", role="hod", subject="Electrical")

    iiot = User(username="iiot_hod", password="123", role="hod", subject="IIOT")

    # Add users to database
    db.session.add(admin)
    db.session.add(cs)
    db.session.add(civil)
    db.session.add(it)
    db.session.add(ece)
    db.session.add(electrical)
    db.session.add(iiot)

    db.session.commit()

print("Users Created Successfully")