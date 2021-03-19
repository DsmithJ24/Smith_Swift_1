import Data
import Data_GUI
import os

DATA_MINIMUM = 1000


def test_data_entries():
    data = Data.get_api_data()
    assert len(data) >= DATA_MINIMUM


def test_states():
    data = Data.get_excel_data("state_M2019_dl.xlsx")
    states = []
    for entries in data:
        if entries['area_title'] in states:
            pass
        else:
            states.append(entries['area_title'])
    # all 50?
    assert len(states) >= 50
    # includes territories +DC too
    assert len(states) <= 54


def test_table_names():
    # test to see if new table exists
    # test to see if old table exists
    clear_db()
    conn, cursor = Data.open_DB("test_db.sqlite")
    Data.setup_DB_schools(cursor)
    Data.setup_DB_jobs(cursor)

    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')

    res = cursor.fetchall()

    assert len(res) == 2

    test_res = res[0]
    assert test_res[0] == 'occupation'
    test_res = res[1]
    assert test_res[0] == 'schools'

def test_store_data():
    # this is a modified version of the shared answer for Sprint 2 with the additional field for
    # excel data since the store function is used for both and takes both parameters, test from
    # before will be the same. Test for the jobs data will be very similar.

    clear_db()
    # make the database first
    conn, cursor = Data.open_DB("test_db.sqlite")
    Data.setup_DB_schools(cursor)
    Data.setup_DB_jobs(cursor)

    # make a test entry to put into the DB
    # need Name, City, 2018 size, 2017 size, 2017 earnings, 2016 repayment
    test_api_data = [{'school.name': 'Test University', 'school.city': 'Boston', '2018.student.size': 1000,
                  '2017.student.size': 900,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004}]

    # make a test entry for the jobs table and put into DB
    test_excel_data = [{'area_title': 'Mass', 'occ_title': 'Management', 'o_group': 'major', 'tot_emp': 7000,
                        'h_pct25': 25.89, 'a_pct25': 50000, 'occ_code': '11-7890'}, {'area_title': 'Maine',
                        'occ_title': 'Developer', 'o_group': 'random', 'tot_emp': 800, 'h_pct25': 30.78,
                        'a_pct25': 100000, 'occ_code': '45-3410'}, {'area_title': 'Iowa', 'occ_title': 'Farmer',
                        'o_group': 'major', 'tot_emp': 1000, 'h_pct25': 20.58, 'a_pct25': 40000,
                        'occ_code': '32-7591'}]

    # now put it into the DB
    Data.store_In_DB(test_api_data, test_excel_data, cursor)

    # close DB
    Data.close_DB(conn)

    # now check if it is in DB
    conn, cursor = Data.open_DB("test_db.sqlite")

    # get the stuff from the DB
    # check school table first

    # the sqlite_master table is a metadata table with information about all the tables in it
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'school_%';''')
    # like does pattern matching with % as the wildcard

    res = cursor.fetchall()
    assert len(res) == 1

    cursor.execute('''SELECT school_name FROM schools''')
    res = cursor.fetchall()
    test_res = res[0]  # seems to et rid of ('',) from res
    assert test_res[0] == 'Test University'

    # now for jobs table
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'occu_%';''')

    # does not work...
    res = cursor.fetchall()
    assert len(res) == 1

    # this works
    cursor.execute('''SELECT state_name FROM occupation''')
    res = cursor.fetchall()
    test_eres = res[0]
    assert test_eres[0] == 'Mass'
    test_eres = res[1]
    assert test_eres[0] == 'Iowa'

    Data.close_DB(conn)

def test_jobs_analysis():
    setup_test_db()
    test_jobs = Data_GUI.get_job_data("test_db.sqlite")
    # Maine and Puerto Rico have graduates but no jobs
    assert test_jobs[24]['graduates'] == 500
    assert test_jobs[24]['jobs'] == 0
    assert test_jobs[24]['jobs_vs_graduates'] == -500

    assert test_jobs[44]['graduates'] == 419
    assert test_jobs[44]['jobs'] == 500
    assert test_jobs[44]['jobs_vs_graduates'] == 81

    # Mass and Iowa have no graduates, but have jobs
    assert test_jobs[22]['graduates'] == 0
    assert test_jobs[22]['jobs'] == 7000
    assert test_jobs[22]['jobs_vs_graduates'] == 7000

    assert test_jobs[15]['graduates'] == 135
    assert test_jobs[15]['jobs'] == 1000
    assert test_jobs[15]['jobs_vs_graduates'] == 865


def test_repayment_analysis():
    setup_test_db()
    test_repayment = Data_GUI.get_repayment_data("test_db.sqlite")
    # will only get data for Puerto Rico (PR), only entry with occ_code beginning with 00
    assert test_repayment[1]['state'] == 'PR'
    assert test_repayment[1]['school_name'] == 'Test University 3'
    assert test_repayment[1]['job_title'] == 'EPA'
    assert test_repayment[1]['bad_repayment_odds'] == 166753.24675324676

    assert test_repayment[0]['state'] == 'IA'
    assert test_repayment[0]['school_name'] == 'Test University 5'
    assert test_repayment[0]['job_title'] == 'Farmer'
    assert test_repayment[0]['bad_repayment_odds'] == 81632.6530612245


def test_jobs_increasing():
    setup_test_db()
    test_jobs_1 = Data_GUI.get_job_data("test_db.sqlite")
    test_jobs = Data_GUI.sort_jobs_increasing(test_jobs_1)

    # Maine has no jobs so will be somewhere in list. No time to try to figure out where, look at easier ones

    assert test_jobs[56]['graduates'] == 419
    assert test_jobs[56]['jobs'] == 500
    assert test_jobs[56]['jobs_vs_graduates'] == 81

    # Mass and Iowa have no graduates, but have jobs
    assert test_jobs[58]['graduates'] == 0
    assert test_jobs[58]['jobs'] == 7000
    assert test_jobs[58]['jobs_vs_graduates'] == 7000

    assert test_jobs[57]['graduates'] == 135
    assert test_jobs[57]['jobs'] == 1000
    assert test_jobs[57]['jobs_vs_graduates'] == 865


def test_job_decreasing():
    setup_test_db()
    test_jobs_1 = Data_GUI.get_job_data("test_db.sqlite")
    test_jobs = Data_GUI.sort_jobs_decreasing(test_jobs_1)

    assert test_jobs[2]['graduates'] == 419
    assert test_jobs[2]['jobs'] == 500
    assert test_jobs[2]['jobs_vs_graduates'] == 81

    # Mass and Iowa have no graduates, but have jobs
    assert test_jobs[0]['graduates'] == 0
    assert test_jobs[0]['jobs'] == 7000
    assert test_jobs[0]['jobs_vs_graduates'] == 7000

    assert test_jobs[1]['graduates'] == 135
    assert test_jobs[1]['jobs'] == 1000
    assert test_jobs[1]['jobs_vs_graduates'] == 865


def test_increasing_repayment():
    setup_test_db()
    test_repayment_1= Data_GUI.get_repayment_data("test_db.sqlite")
    test_repayment = Data_GUI.sort_repayment_increasing(test_repayment_1)

    assert test_repayment[1]['state'] == 'PR'
    assert test_repayment[1]['school_name'] == 'Test University 3'
    assert test_repayment[1]['job_title'] == 'EPA'
    assert test_repayment[1]['bad_repayment_odds'] == 166753.24675324676

    assert test_repayment[0]['state'] == 'IA'
    assert test_repayment[0]['school_name'] == 'Test University 5'
    assert test_repayment[0]['job_title'] == 'Farmer'
    assert test_repayment[0]['bad_repayment_odds'] == 81632.6530612245


def test_decreasing_repayment():
    setup_test_db()
    test_repayment_1= Data_GUI.get_repayment_data("test_db.sqlite")
    test_repayment = Data_GUI.sort_repayment_decreasing(test_repayment_1)

    assert test_repayment[0]['state'] == 'PR'
    assert test_repayment[0]['school_name'] == 'Test University 3'
    assert test_repayment[0]['job_title'] == 'EPA'
    assert test_repayment[0]['bad_repayment_odds'] == 166753.24675324676

    assert test_repayment[1]['state'] == 'IA'
    assert test_repayment[1]['school_name'] == 'Test University 5'
    assert test_repayment[1]['job_title'] == 'Farmer'
    assert test_repayment[1]['bad_repayment_odds'] == 81632.6530612245

def clear_db():
    if os.path.exists("test_db.sqlite"):
        os.remove("test_db.sqlite")

def setup_test_db():
    clear_db()
    conn, cursor = Data.open_DB("test_db.sqlite")
    Data.setup_DB_schools(cursor)
    Data.setup_DB_jobs(cursor)

    test_api_data = [{'school.name': 'Test University 1', 'school.city': 'Boston', '2018.student.size': 1000,
                      '2017.student.size': 900,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                      '2016.repayment.3_yr_repayment.overall': 4004, 'school.state': 'Mass',
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 0.789},
                     {'school.name': 'Test University 2', 'school.city': 'Portland', '2018.student.size': 800,
                      '2017.student.size': 700,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 539,
                      '2016.repayment.3_yr_repayment.overall': 2874, 'school.state': 'Maine',
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 0.261},
                     {'school.name': 'Test University 3', 'school.city': 'San Juan', '2018.student.size': 1676,
                      '2017.student.size': 1520,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 205,
                      '2016.repayment.3_yr_repayment.overall': 1835, 'school.state': 'PR',
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 0.924},
                     {'school.name': 'Test University 4', 'school.city': 'Augusta', '2018.student.size': 1200,
                      '2017.student.size': 1100,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 673,
                      '2016.repayment.3_yr_repayment.overall': 3024, 'school.state': 'ME',
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 0.261},
                     {'school.name': 'Test University 5', 'school.city': 'De Mois', '2018.student.size': 540,
                      '2017.student.size': 320,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 345,
                      '2016.repayment.3_yr_repayment.overall': 4635, 'school.state': 'IA',
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 0.490},
                     ]

    # make a test entry for the jobs table and put into DB
    test_excel_data = [{'area_title': 'Massachusetts', 'occ_title': 'Management', 'o_group': 'major', 'tot_emp': 7000,
                        'h_pct25': 25.89, 'a_pct25': 50000, 'occ_code': '13-7890'},
                       {'area_title': 'Maine', 'occ_title': 'Developer', 'o_group': 'random', 'tot_emp': 800,
                        'h_pct25': 30.78, 'a_pct25': 100000, 'occ_code': '45-3410'},
                       {'area_title': 'Iowa', 'occ_title': 'Farmer', 'o_group': 'major', 'tot_emp': 1000,
                        'h_pct25': 20.58, 'a_pct25': 40000, 'occ_code': '00-7591'},
                       {'area_title': 'PR', 'occ_title': 'EPA', 'o_group': 'major', 'tot_emp': 500, 'h_pct25': 50.67,
                        'a_pct25': 154080, 'occ_code': '00-3287'}]

    Data.store_In_DB(test_api_data, test_excel_data, cursor)

    # close DB
    Data.close_DB(conn)