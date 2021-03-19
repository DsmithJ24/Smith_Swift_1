
import secrets
import requests
import json

import sqlite3
from typing import Tuple

import pandas as pd
import os

from typing import List, Dict

url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
# outfile = open(r"api_data.txt", "w")

# prevents error reading the file
pre = os.path.dirname(os.path.realpath(__file__))

def get_api_data():
    all_data = []
    page = 0
    next_page = True

    # Stops if it hits a false
    while next_page != False:
        # print(page)
        response = requests.get(f"{url}school.degrees_awarded.predominant=2,3&fields=school.name,school.city,"
                                f"2018.student.size,2017.student.size,"
                                f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall,school.state,"
                                f"2016.repayment.repayment_cohort.3_year_declining_balance"
                                f"&api_key={secrets.api_key}&page={page}")
        if response.status_code != 200:
            print("Error getting data!")
            # do not exit, continue. Don't get stuck at one point. Rather miss data than endless loop
            page = page + 1
            continue

        # following code puts data in .json format
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
        next_page = check_page(page_of_school_data)
        page=page+1
    # print("Total number of pages is", page)
    return all_data

def get_excel_data(name:str):
    # area_type 2 is for state, 3 is for territory
    # o group must be 'major', bad options are total and detailed

    # need:
    # state, occupation major title, total employment in that field in that state
    # 25th percentile salary (assume college grads in lower 25%) for field both hourly AND annually
    # and occupation code
    # ToDo this value will be changed, don't make it a global
    filename = name
    path = os.path.join(pre, filename)

    excel = pd.read_excel(path, engine='openpyxl')

    df = pd.DataFrame(excel, columns=['area_title', 'occ_title', 'o_group', 'tot_emp', 'h_pct25', 'a_pct25', 'occ_code'])
    df = df[df.o_group != 'detailed']
    data = df.to_json(orient='records')
    parsed_data = json.loads(data)
    return parsed_data

def check_page(page):
    if len(page) < 20:
        return False
    elif len(page) > 20:
        print("Entries exceed page!!!")
        pass
    else:
        pass

def open_DB(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    # Create a DB if one does not exist (will do this always for now), or connect to one
    db_connection = sqlite3.connect(filename)
    # prepare to read/write data
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_DB(connection:sqlite3.Connection):
    # save any changes
    connection.commit()
    # close the connection
    connection.close()

def setup_DB_schools(cursor:sqlite3.Cursor):
    # create columns labeled after the 6 parameters
    # name DB after schools. Can't start with numbers
    # first 2 are strings,when entered, must have ?
    # others can just enter data automatically
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools(
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT 0,
    student_size_2017 INTEGER DEFAULT 0,
    over_poverty_after_3_years_2017 INTEGER DEFAULT 0,
    repayment_overall_2016 INTEGER DEFAULT 0,
    school_state TEXT NOT NULL,
    repayment_declining_2016 INTEGER DEFAULT 0
    );''')

def setup_DB_jobs(cursor:sqlite3.Cursor):
    # need:
    # state, occupation major title, total employment in that field in that state
    # 25th percentile salary (assume college grads in lower 25%) for field both hourly and annually
    # and occupation code

    cursor.execute('''CREATE TABLE IF NOT EXISTS occupation(
    state_name TEXT NOT NULL,
    occupation_title TEXT NOT NULL,
    employment_in_field INTEGER,
    hour_salary_25th_percentile DOUBLE,
    annual_salary_25th_percentile INTEGER,
    occupation_code TEXT NOT NULL
    );''')

def check_api_data(data: List[Dict]):
    # checks to make sure data with expected integers have 0s instead of None
    # check to see if int values are null
    # maybe just replace value with 0, cannot do elif. Must be ifs
    for i in range(len(data)):
        if data[i]['2018.student.size'] is None:
            data[i]['2018.student.size'] = 0

        if data[i]['2017.student.size'] is None:
            data[i]['2017.student.size'] = 0

        if data[i]['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'] is None:
            data[i]['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'] = 0

        if data[i]['2016.repayment.3_yr_repayment.overall'] is None:
            data[i]['2016.repayment.3_yr_repayment.overall'] = 0

        if data[i]['2016.repayment.repayment_cohort.3_year_declining_balance'] is None:
            data[i]['2016.repayment.repayment_cohort.3_year_declining_balance'] = 0

    #return data

def check_excel_data(data: List[Dict]):
    for i in range(len(data)):
        if data[i]['tot_emp'] is None:
            data[i]['tot_emp'] = 0

        if data[i]['h_pct25'] is None:
            data[i]['h_pct25'] = 0.0

        if data[i]['a_pct25'] is None:
            data[i]['a_pct25'] = 0

    #return data

def store_In_DB(api_data: list, excel_data: list, cursor:sqlite3.Cursor):
    # use the dictionary tiles to put in DB
    # use the ? method, put ? into inputted values and then the dictionary values outside ()
    # this way, the data is a string and not thought of as a column name

    # use for loop
    check_api_data(api_data)
    for adata in api_data:
        # first check to see if any unwanted Nulls

        # check_data(adata)
        # have list[x][param] in the Tuple (after VALUES) where x is entry and para is the column
        # insert data, need as many ?s as columns
        cursor.execute('''INSERT INTO schools(school_name, school_city, school_state, 
        student_size_2018, student_size_2017, over_poverty_after_3_years_2017, repayment_overall_2016, 
        repayment_declining_2016)
        VALUES (?,?,?,?,?,?,?,?)''',
                       (adata['school.name'], adata['school.city'], adata['school.state'],
                        adata['2018.student.size'], adata['2017.student.size'],
                        adata['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                        adata['2016.repayment.3_yr_repayment.overall'],
                        adata['2016.repayment.repayment_cohort.3_year_declining_balance']))

    for edata in excel_data:

        # want one last check to see if any non major o_groups have snuck in
        # this check just wiped the data...
        if edata['o_group'] != 'detailed':
            cursor.execute('''INSERT INTO occupation(state_name, occupation_title,
            employment_in_field, hour_salary_25th_percentile, annual_salary_25th_percentile,
            occupation_code) VALUES(?,?,?,?,?,?)''',
                           (edata['area_title'], edata['occ_title'], edata['tot_emp'],
                            edata['h_pct25'], edata['a_pct25'], edata['occ_code']))

# ToDO: Create a GUI for the data
#  GUI should allow user to update the data or visualize data
#  will also need a separate file for the window

# ToDO: data analysis
#  user chooses following data for map or text visualization
#  1) compare numb of college grads in a state with number of jobs in state that expect college education.
#  For this remove professions with occ_code beginning with 30-39 or 40-49
#  2) compare 3 year graduate cohort declining balance to the 25% salary in the state


def main(file_name: str):
    if os.path.exists("sprint_db.sqlite"):
        os.remove("sprint_db.sqlite")

    api_data = get_api_data()

    print("Api data retrieved!")

    excel_data = get_excel_data(file_name)
    print("Excel data retrieved! Storing data...")

    '''
    # these next few lines are for an older version. May still want them in comments
    print(json.dumps(demo_data, indent=6), file=outfile)
    # will create a .txt file with 25626 lines. 25626/8 = 3203 entries as expected
    outfile.close()
    print("Data has been saved to a file")
    # print(json.dumps(excel_data, indent=6), file=outfile)
    # outfile.close()
    '''

    conn, cursor = open_DB("sprint_db.sqlite")
    setup_DB_schools(cursor)
    setup_DB_jobs(cursor)

    store_In_DB(api_data, excel_data, cursor)
    print("Data has been stored in the Database!")

    close_DB(conn)



if __name__ == '__main__':
    main("state_M2019_dl.xlsx")

