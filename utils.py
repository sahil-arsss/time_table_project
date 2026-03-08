import pandas as pd
from models import Timetable, db

def parse_excel(filepath):

    excel = pd.ExcelFile(filepath)

    for sheet in excel.sheet_names:

        df = pd.read_excel(filepath, sheet_name=sheet)

        periods = df.columns[1:]

        for i in range(1, len(df)):

            day = df.iloc[i,0]

            for j,period in enumerate(periods):

                dept = df.iloc[i,j+1]

                if pd.isna(dept):
                    continue

                entry = Timetable(
                    room=sheet,
                    day=day,
                    period=period,
                    department=str(dept),
                    subject="",
                    professor=""
                )

                db.session.add(entry)

    db.session.commit()