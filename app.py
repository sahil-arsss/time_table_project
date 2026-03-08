from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db, User, Timetable
from utils import parse_excel
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            login_user(user)

            if user.role == "admin":
                return redirect("/admin")

            return redirect("/hod")

    return render_template("login.html")


@app.route("/admin", methods=["GET","POST"])
@login_required
def admin():

    if request.method == "POST":

        file = request.files["file"]

        path = os.path.join("uploads", file.filename)

        file.save(path)

        parse_excel(path)

    data = Timetable.query.all()

    return render_template("admin_dashboard.html", data=data)


@app.route("/hod")
@login_required
def hod():

    return render_template("hod_dashboard.html")


@app.route("/view_all")
@login_required
def view_all():

    data = Timetable.query.all()

    return render_template("view_all.html", data=data)


@app.route("/my_subject")
@login_required
def my_subject():

    data = Timetable.query.filter_by(department=current_user.subject).all()

    return render_template("my_subject.html", data=data)


@app.route("/edit/<id>", methods=["GET","POST"])
@login_required
def edit(id):

    entry = Timetable.query.get(id)

    if entry.department != current_user.subject:
        return "Not Allowed"

    if request.method == "POST":

        entry.subject = request.form["subject"]

        entry.professor = request.form["professor"]

        db.session.commit()

        return redirect("/my_subject")

    return render_template("edit_table.html", entry=entry)


@app.route("/timetable", methods=["GET","POST"])
@login_required
def timetable():

    dept = current_user.subject

    data = Timetable.query.filter_by(department=dept).all()

    if request.method == "POST":

        entry_id = request.form["id"]

        subject = request.form["subject"]

        professor = request.form["professor"]

        entry = Timetable.query.get(entry_id)

        entry.subject = subject

        entry.professor = professor

        db.session.commit()

        return redirect("/timetable")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

    periods = ["P1","P2","P3","P4","P5","P6","P7","P8"]

    return render_template(
        "timetable_view.html",
        data=data,
        days=days,
        periods=periods
    )    
    
    
@app.route("/export_pdf")
@login_required
def export_pdf():

    dept = current_user.subject

    data = Timetable.query.filter_by(department=dept).all()

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

    periods = ["P1","P2","P3","P4","P5","P6","P7","P8"]

    table_data = []

    header = ["Day"] + periods
    table_data.append(header)

    for day in days:

        row = [day]

        for p in periods:

            cell_text = ""

            for e in data:

                if e.day == day and e.period == p:

                    cell_text += f"{e.room}\n{e.subject}\n{e.professor}\n"

            row.append(cell_text)

        table_data.append(row)

    file = "timetable.pdf"

    pdf = SimpleDocTemplate(file)

    table = Table(table_data)

    # ADD GRID STYLE HERE
    style = TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE")
    ])

    table.setStyle(style)

    pdf.build([table])

    return send_file(file, as_attachment=True)



@app.route("/logout")
def logout():

    logout_user()

    return redirect("/")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)