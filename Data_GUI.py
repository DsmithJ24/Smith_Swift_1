import openpyxl
import PySide6.QtWidgets
import sys
import Data
import Data_Window
import numbers
import sqlite3
import json
from typing import List, Dict

# This file seems to take in data. other file does the stuff with the data

def display_data(data: list):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)
    my_window = Data_Window.MainWindow(data)
    sys.exit(qt_app.exec_())


def get_data() -> List[Dict]:

    # ToDO: when updating let user choose a file name or just take excel file.
    #  Later in project, make it so the wb name is a variable that takes an input.
    #  This data will be from sprint 3 Database, not the contents of the file itself

    Data.main()

    conn = sqlite3.connect('sprint_db.sqlite')
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute('''SELECT * FROM schools''').fetchall()
    job_rows = database.execute('''SELECT * FROM occupation''').fetchall()

    conn.commit()
    conn.close()

    schools = json.dumps([dict(ix) for ix in school_rows])
    jobs = json.dumps([dict(iy) for iy in job_rows])

    # ToDo: need most recent college grads and declining balance from school table
    #  and jobs (occ_code not starting with 30-39 or 40-49) plus 25% percent salary from jobs table

    workbook_file = openpyxl.load_workbook("state_M2019_dl.xlsx")
    worksheet = workbook_file.active
    data_list = []
    for current_row in worksheet.rows:
        state_cell = current_row[1]
        state_name = state_cell.value
        hourly_salary_25_percentage = current_row[19].value
        if not isinstance(hourly_salary_25_percentage, numbers.Number):
            continue
        record = {"state_name": state_name, "hourly_salary": hourly_salary_25_percentage}
        data_list.append(record)
    return data_list


def get_key(value:dict):
    return value["hourly_salary"]


# ToDo: next two funcs may be changed and/or put in Data.py
def main():
    data = get_data()
    data.sort(key=get_key)  # sorts from highest salary to lowest
    display_data(data)


if __name__ == '__main__':
    main()
