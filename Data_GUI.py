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

    # ToDo: pass a file name into this
    Data.main("state_M2019_dl.xlsx")

    conn = sqlite3.connect('sprint_db.sqlite')
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute('''SELECT * FROM schools''').fetchall()
    job_rows = database.execute('''SELECT * FROM occupation''').fetchall()

    conn.commit()
    conn.close()

    #schools = json.loads(school_rows)
    #jobs = json.loads(job_rows)

    # ToDo: need most recent college grads and declining balance from school table
    #  and jobs (occ_code not starting with 30-39 or 40-49) plus 25% percent salary from jobs table

    data_list = []

    for sdata in school_rows:
        size_total = sdata['student_size_2018']
        #size_total = size_cell.value
        if not isinstance(size_total, numbers.Number):
            continue

        declining_balance = sdata['repayment_declining_2016']
        if not isinstance(declining_balance, numbers.Number):
            continue
        record = {"total students": size_total, "3 year balance": declining_balance}
        data_list.append(record)

    # ToDO these dont seem to be added to the datalist....
    for jdata in job_rows:
        ooc_codes = jdata['occupation_code']
        hourly_salary = jdata['hour_salary_25th_percentile']
        record = {"occ_code": ooc_codes, "hourly_salary": hourly_salary}
        data_list.append(record)

    return data_list

'''
def get_key(value:dict):
    return value["hourly_salary"]
'''

# ToDo: next two funcs may be changed and/or put in Data.py
def main():
    data = get_data()
    # data.sort(key=get_key)  # sorts from highest salary to
    display_data(data)


if __name__ == '__main__':
    main()
