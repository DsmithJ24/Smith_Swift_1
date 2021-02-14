import secrets
import requests
# import json

import sqlite3
from typing import Tuple

DATA_MINIMUM = 1000

# when using debugger, wait a sec for everything to load
url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
# outfile = open(r"api_data.txt", "w")

def get_data():
    # will retrieve:
    # school name
    # school city
    # 2018 student size
    # 2017 student size
    # 2017 earnings (3 years after completion.overall count over poverty line)
    # 2016 repayment (3 year repayment.overall)

    all_data = []
    page = 0
    nextPage = True

    # Stops if it hits a false
    while nextPage != False:
        # print(page)
        # put additional fields after &fields=
        response = requests.get(f"{url}school.degrees_awarded.predominant=2,3&fields=school.name,school.city,"
                                f"2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}&page={page}") #put the api url here
        if response.status_code != 200:
            print("Error getting data!")
            # do not exit, continue. Don't get stuck at one point
            page = page + 1
            continue

        # following code puts data in .json format
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
        nextPage = check_page(page_of_school_data)
        page=page+1
    # print("Total number of pages is", page)
    return all_data, page

def check_page(page):
    if len(page) < 20:
        return False
    elif len(page) > 20:
        print("Entries exceed page!!!")
        pass
    else:
        pass

def check_data_entries(data, pages):
    print("Total number of pages is", pages)
    length = len(data)
    if length < DATA_MINIMUM:
        print(f"Less than {DATA_MINIMUM} entries! Ending")
        # end program?
        exit(-1)
    else:
        print(f"Data has {length} entries. Data will now be stored.")

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

def setup_DB(cursor:sqlite3.Cursor):
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
    repayment_overall_2016 INTEGER DEFAULT 0
    );''')
    # what if last column is a TEXT NOT NULL?


def store_In_DB(api_data, cursor:sqlite3.Cursor):
    # takes the fetched data and stores in a DB
    # store data in the DB (while loop), use the all_data array?

    # use the dictionary tiles to put in DB (no while loop?)
    # use the ? method, put ? into inputted values and then the dictionary values outside ()
    # this way, the data is a string and not thought of as a column name

    # use while loop
    # look up list dictionary, use '?' method, check if number data has null (None) set to 0 if is
    entry = 0
    while entry < len(api_data):
        # have list[x][param] in the Tuple (after VALUES) where x is entry and para is the column
        # check to see if int values are null, start with only the 2018 size for now
        # maybe just replace value with 0, cannot do elif. Must be ifs
        if api_data[entry]['2018.student.size'] == None:
            api_data[entry]['2018.student.size'] = 0

        if api_data[entry]['2017.student.size'] == None:
            api_data[entry]['2017.student.size'] = 0

        if api_data[entry]['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'] == None:
            api_data[entry]['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'] = 0

        if api_data[entry]['2016.repayment.3_yr_repayment.overall'] == None:
            api_data[entry]['2016.repayment.3_yr_repayment.overall'] = 0

        # insert data
        # need 6 ?s
        cursor.execute(f'''INSERT INTO SCHOOLS (school_name, school_city, 
        student_size_2018, student_size_2017, over_poverty_after_3_years_2017, repayment_overall_2016)
        VALUES (?,?,?,?,?,?)''',
                       (api_data[entry]['school.name'], api_data[entry]['school.city'],
                        api_data[entry]['2018.student.size'], api_data[entry]['2017.student.size'],
                        api_data[entry]['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                        api_data[entry]['2016.repayment.3_yr_repayment.overall']))
        entry = entry + 1

def main():
    # saves the data to a new table, used this to save into DB
    demo_data, pages = get_data()
    # test to see if >1000 entries. If not, exit
    check_data_entries(demo_data, pages)

    '''
    # these next few lines are for an older version. May still want them in comments
    print(json.dumps(demo_data, indent=6), file=outfile)
    # will create a .txt file with 25626 lines. 25626/8 = 3203 entries as expected
    outfile.close()
    print("Data has been saved to a file")
    '''

    conn, cursor = open_DB("demo_db.sqlite")
    setup_DB(cursor)
    print(type(conn))
    store_In_DB(demo_data, cursor)
    print("Data has been stored in the Database!")
    close_DB(conn)

if __name__ == '__main__':
    main()