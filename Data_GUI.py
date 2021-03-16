import os

import PySide6.QtWidgets
import sys
import Data
import Data_Window
import numbers
import sqlite3
import json
from typing import List, Dict

# This file seems to take in data. other file does the stuff with the data


def display_data():
    # ToDo: have this return data from get data and return it
    '''
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)
    my_window = Data_Window.MainWindow()
    sys.exit(qt_app.exec_())
    '''
    received_data = get_data()
    return received_data


def find_file(file_name:str):
    pre = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(pre, file_name)
    try:
        file = open(path)
        file.close()
        return True
    except FileNotFoundError:
        return False

def get_data() -> List[Dict]:
    '''
    # ToDo: pass a file name into this
    Data.main("state_M2019_dl.xlsx")

    conn = sqlite3.connect('sprint_db.sqlite')
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute(''
    'SELECT * FROM schools'
    '').fetchall()
    job_rows = database.execute(''
    'SELECT * FROM occupation'
    '').fetchall()

    conn.commit()
    conn.close()


    #schools = json.loads(school_rows)
    #jobs = json.loads(job_rows)

    # ToDo: need most recent college grads and declining balance from school table
    #  and jobs (occ_code not starting with 30-39 or 40-49) plus 25% percent salary from jobs table

    data_list = []
    school_list = []
    job_list = []

    for sdata in school_rows:
        size_total = sdata['student_size_2018']
        declining_balance = sdata['repayment_declining_2016']
        school_state = sdata['school_state']
        record = {"state": school_state, "total students": size_total, "3 year balance": declining_balance}
        school_list.append(record)

    # ToDO these dont seem to be added to the datalist....
    for jdata in job_rows:
        ooc_codes = jdata['occupation_code']
        hourly_salary = jdata['hour_salary_25th_percentile']
        job_state = jdata['state_name']
        record = {"state": job_state, "occ_code": ooc_codes, "hourly_salary": hourly_salary}
        job_list.append(record)

    '''

    test_list = []

    record = {"total students": 100, "3 year balance": 3000, "occ_code": 45-679, "hourly salary": 15}
    test_list.append(record)
    return test_list


def get_key(value:dict):
    return value["hourly_salary"]


# ToDo: next two funcs may be changed and/or put in Data.py
def main():
    '''
    data = get_data()
    #school_data.sort(key=get_key)  # sorts from highest salary to
    #job_data.sort(key=get_key())
    display_data(data)
    '''
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)
    my_window = Data_Window.MainWindow()
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()
