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

    # ToDo: pass a file name into this
    #Data.main("state_M2019_dl.xlsx")

    conn = sqlite3.connect('sprint_db.sqlite')
    conn.row_factory = sqlite3.Row
    database = conn.cursor()

    school_rows = database.execute('''SELECT * FROM schools''').fetchall()
    job_rows = database.execute('''SELECT * FROM occupation''').fetchall()

    conn.commit()
    conn.close()

    #schools = json.loads(school_rows)
    #jobs = json.loads(job_rows)

    # ToDo: get the number of all college graduates (student_size/4) from a state
    #  and jobs (occ_code not starting with 30-39 or 40-49)

    data_list = []
    '''

    for entries in school_rows:
        if entries['school_state'] in states:
            pass
        else:
            states.append(entries['school_state'])
    states.sort()

    # map states to abbreviations
    '''

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
              {'State': 'Wisconsin', 'Abbreviation': 'WI'},{'State': 'West Virginia', 'Abbreviation': 'WV'},
              {'State': 'Wyoming', 'Abbreviation': 'WY'}]

    # terriories: VI- virgin islands, PW-palau, PR-puerto rico, MP- mariana islands,
    # MH- marshall islands, GU-guam, FM-micronesia, DC- washDC, AS- american samoa
    graduate_list = []
    # states outside, school_states inside

    for y in range(len(states)):
        graduates = 0
        for x in range(len(school_rows)):
            if states[y]['State'] == school_rows[x]['school_state'] or states[y]['Abbreviation'] ==\
                    school_rows[x]['school_state']:
                school_graduates = school_rows[x]['student_size_2018']
                # ToDo: change stuff in Data.py so no nulls are saved. Used above lines as reference
                if school_graduates is None:
                    school_graduates = 0
                graduates = school_graduates + graduates
        graduate_list.append(graduates)

    print(graduate_list)
    '''    
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
