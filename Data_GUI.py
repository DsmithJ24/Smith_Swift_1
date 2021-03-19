import os

import PySide6.QtWidgets
import sys
import Data
import Data_Window
import sqlite3
from typing import List, Dict

# This file seems to take in data. other file does the stuff with the data


def display_data(database_name):
    job_data = get_job_data(database_name)
    payment_data = get_repayment_data(database_name)
    return job_data, payment_data


def find_file(file_name: str):
    pre = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(pre, file_name)
    try:
        file = open(path)
        file.close()
        return True
    except FileNotFoundError:
        return False


def initialize_db(file_name):
    Data.main(file_name)


def get_job_data(database_name: str) -> List[Dict]:
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute('''SELECT * FROM schools''').fetchall()
    job_rows = database.execute('''SELECT * FROM occupation''').fetchall()

    conn.commit()
    conn.close()

    data = []

    states = get_all_states()
    # terriories: VI- virgin islands, PW-palau, PR-puerto rico, MP- mariana islands,
    # MH- marshall islands, GU-guam, FM-micronesia, DC- washDC, AS- american samoa

    graduate_total = []
    for y in range(len(states)):
        graduates = 0
        for x in range(len(school_rows)):
            if states[y]['State'] == school_rows[x]['school_state'] or states[y]['Abbreviation'] ==\
                    school_rows[x]['school_state']:
                school_graduates = (school_rows[x]['student_size_2018'])/4
                if school_graduates is None:
                    school_graduates = 0
                graduates = school_graduates + graduates
        graduate_total.append(graduates)

    all_of_states = []
    for s in states:
        all_of_states.append(s['State'])

    excel_states = []
    for y in job_rows:
        excel_states.append(y['state_name'])

    states_to_add = []
    for i in range(len(states)):
        if all_of_states[i] not in excel_states:
            missing_state = all_of_states[i]
            states_to_add.append(missing_state)

    jobs_total = []
    for y in range(len(states)):
        jobs = 0
        for x in range(len(job_rows)):
            if states[y]['State'] == job_rows[x]['state_name'] or states[y]['Abbreviation'] ==\
                    job_rows[x]['state_name']:
                if job_rows[x]['occupation_code'][0:1] != '3' and job_rows[x]['occupation_code'][0:1] != '4':
                    occupation_jobs = job_rows[x]['employment_in_field']
                    if occupation_jobs is None:
                        occupation_jobs = 0
                    jobs = occupation_jobs + jobs
        jobs_total.append(jobs)

    '''
    test_list = []

    record = {"total students": 100, "3 year balance": 3000, "occ_code": 45-679, "hourly salary": 15}
    test_list.append(record)
    return test_list
    '''

    for size in range(len(states)):
        jobs_vs_graduates = jobs_total[size] - graduate_total[size]
        record = {"state": all_of_states[size], "graduates": graduate_total[size], "jobs": jobs_total[size],
                  "jobs_vs_graduates": jobs_vs_graduates}
        data.append(record)

    return data


def get_repayment_data(database_name: str) -> List[Dict]:
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute('''SELECT * FROM schools''').fetchall()
    job_rows = database.execute('''SELECT * FROM occupation''').fetchall()

    conn.commit()
    conn.close()

    states = get_all_states()

    school_data = []
    data = []
    for i in range(len(school_rows)):
        school_record = {"school_name": school_rows[i]['school_name'], "school_state": school_rows[i]['school_state'],
                         "school_declining_repayment": school_rows[i]['repayment_declining_2016']}
        school_data.append(school_record)

    # print(school_data)
    for x in range(len(states)):
        for y in range(len(job_rows)):
            if states[x]['State'] == job_rows[y]['state_name'] or states[x]['Abbreviation'] ==\
                    job_rows[y]['state_name']:
                current_state = states[x]['Abbreviation']
                for z in range(len(school_data)):
                    if current_state == school_data[z]["school_state"]:
                        if job_rows[y]['occupation_code'][0:2] == '00':
                            school_bad_repayment = school_data[z]["school_declining_repayment"]
                            annual_salary = job_rows[y]['annual_salary_25th_percentile']
                            if school_bad_repayment == 0:
                                salary_vs_bad_repayment = 0
                            else:
                                salary_vs_bad_repayment = annual_salary/school_bad_repayment
                            record = {"state": current_state, "school_name": school_data[z]["school_name"],
                                      "job_title": job_rows[y]['occupation_title'],
                                      "bad_repayment_odds": salary_vs_bad_repayment}
                            data.append(record)
    return data


def get_job_key(value: dict):
    return value["jobs"]


def get_repayment_key(value: dict):
    return value["bad_repayment_odds"]


def sort_jobs_increasing(data: List[Dict]):
    data.sort(key=get_job_key)
    return data


def sort_repayment_increasing(data: List[Dict]):
    data.sort(key=get_repayment_key)
    return data


def sort_jobs_decreasing(data: List[Dict]):
    data.sort(reverse=True, key=get_job_key)
    return data


def sort_repayment_decreasing(data: List[Dict]):
    data.sort(reverse=True, key=get_repayment_key)
    return data

def get_all_states():
    states = [{'State': 'Alabama', 'Abbreviation': 'AK'}, {'State': 'Alaska', 'Abbreviation': 'AL'},
              {'State': 'Arkansas', 'Abbreviation': 'AR'}, {'State': 'American Samoa', 'Abbreviation': 'AS'},
              {'State': 'Arizona', 'Abbreviation': 'AZ'}, {'State': 'California', 'Abbreviation': 'CA'},
              {'State': 'Colorado', 'Abbreviation': 'CO'}, {'State': 'Connecticut', 'Abbreviation': 'CT'},
              {'State': 'District of Columbia', 'Abbreviation': 'DC'}, {'State': 'Delaware', 'Abbreviation': 'DE'},
              {'State': 'Florida', 'Abbreviation': 'FL'}, {'State': 'Micronesia', 'Abbreviation': 'FM'},
              {'State': 'Georgia', 'Abbreviation': 'GA'}, {'State': 'Guam', 'Abbreviation': 'GU'},
              {'State': 'Hawaii', 'Abbreviation': 'HI'}, {'State': 'Iowa', 'Abbreviation': 'IA'},
              {'State': 'Idaho', 'Abbreviation': 'ID'}, {'State': 'Illinois', 'Abbreviation': 'IL'},
              {'State': 'Indiana', 'Abbreviation': 'IN'}, {'State': 'Kansas', 'Abbreviation': 'KS'},
              {'State': 'Kentucky', 'Abbreviation': 'KY'}, {'State': 'Louisiana', 'Abbreviation': 'LA'},
              {'State': 'Massachusetts', 'Abbreviation': 'MA'}, {'State': 'Maryland', 'Abbreviation': 'MD'},
              {'State': 'Maine', 'Abbreviation': 'ME'}, {'State': 'Marshall Islands', 'Abbreviation': 'MH'},
              {'State': 'Michigan', 'Abbreviation': 'MI'}, {'State': 'Minnesota', 'Abbreviation': 'MN'},
              {'State': 'Missouri', 'Abbreviation': 'MO'}, {'State': 'Mariana Island', 'Abbreviation': 'MP'},
              {'State': 'Mississippi', 'Abbreviation': 'MS'}, {'State': 'Montana', 'Abbreviation': 'MT'},
              {'State': 'North Carolina', 'Abbreviation': 'NC'}, {'State': 'North Dakota', 'Abbreviation': 'ND'},
              {'State': 'Nebraska', 'Abbreviation': 'NE'}, {'State': 'New Hampshire', 'Abbreviation': 'NH'},
              {'State': 'New Jersey', 'Abbreviation': 'NJ'}, {'State': 'New Mexico', 'Abbreviation': 'NM'},
              {'State': 'Nevada', 'Abbreviation': 'NV'}, {'State': 'New York', 'Abbreviation': 'NY'},
              {'State': 'Ohio', 'Abbreviation': 'OH'}, {'State': 'Oklahoma', 'Abbreviation': 'OK'},
              {'State': 'Oregon', 'Abbreviation': 'OR'}, {'State': 'Pennsylvania', 'Abbreviation': 'PA'},
              {'State': 'Puerto Rico', 'Abbreviation': 'PR'}, {'State': 'Palau', 'Abbreviation': 'PW'},
              {'State': 'Rhode Island', 'Abbreviation': 'RI'}, {'State': 'South Carolina', 'Abbreviation': 'SC'},
              {'State': 'South Dakota', 'Abbreviation': 'SD'}, {'State': 'Tennessee', 'Abbreviation': 'TN'},
              {'State': 'Texas', 'Abbreviation': 'TX'}, {'State': 'Utah', 'Abbreviation': 'UT'},
              {'State': 'Virginia', 'Abbreviation': 'VA'}, {'State': 'Virgin Islands', 'Abbreviation': 'VI'},
              {'State': 'Vermont', 'Abbreviation': 'VT'}, {'State': 'Washington', 'Abbreviation': 'WA'},
              {'State': 'Wisconsin', 'Abbreviation': 'WI'}, {'State': 'West Virginia', 'Abbreviation': 'WV'},
              {'State': 'Wyoming', 'Abbreviation': 'WY'}]
    return states

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
