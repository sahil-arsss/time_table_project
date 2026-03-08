import pandas as pd
import os
from models import Timetable, db

# remove old data for same room



def parse_excel(filepath):
   
    filename = os.path.basename(filepath)
    room_name = os.path.splitext(filename)[0]   # Room name from file name
    Timetable.query.filter_by(room=room_name).delete()
    db.session.commit()
    ext = os.path.splitext(filepath)[1]

    # CSV FILE
    if ext == ".csv":

        df = pd.read_csv(filepath)

        periods = df.columns[1:]

        for i in range(1, len(df)):

            day = df.iloc[i, 0]

            for j, period in enumerate(periods):

                dept = df.iloc[i, j+1]

                if pd.isna(dept):
                    continue

                entry = Timetable(
                    room=room_name,   # use filename as room
                    day=day,
                    period=period,
                    department=str(dept),
                    subject="",
                    professor=""
                )

                db.session.add(entry)

        db.session.commit()

    # EXCEL FILE
    else:

        excel = pd.ExcelFile(filepath)

        for sheet in excel.sheet_names:

            df = pd.read_excel(filepath, sheet_name=sheet)

            periods = df.columns[1:]

            for i in range(1, len(df)):

                day = df.iloc[i, 0]

                for j, period in enumerate(periods):

                    dept = df.iloc[i, j+1]

                    if pd.isna(dept):
                        continue

                    entry = Timetable(
                        room=sheet,   # room name from sheet
                        day=day,
                        period=period,
                        department=str(dept),
                        subject="",
                        professor=""
                    )

                    db.session.add(entry)

        db.session.commit()