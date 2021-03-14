import Data

DATA_MINIMUM = 1000


def test_data_entries():
    data = Data.get_api_data()
    assert len(data) >= DATA_MINIMUM


def test_states():
    data = Data.get_excel_data()
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
    conn, cursor = Data.open_DB("test_db.sqlite")
    Data.setup_DB_schools(cursor)
    Data.setup_DB_jobs(cursor)

    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')

    res = cursor.fetchall()

    assert len(res) == 2

    test_res = res[0]
    assert test_res[0] == 'schools'
    test_res = res[1]
    assert test_res[0] == 'occupation'


def test_store_data():
    # this is a modified version of the shared answer for Sprint 2 with the additional field for
    # excel data since the store function is used for both and takes both parameters, test from
    # before will be the same. Test for the jobs data will be very similar.

    # make the database first
    conn, cursor = Data.open_DB("test_db.sqlite")
    Data.setup_DB_schools(cursor)
    Data.setup_DB_jobs(cursor)

    # make a test entry to put into the DB
    # need Name, City, 2018 size, 2017 size, 2017 earnings, 2016 repayment
    test_api_data = [{'school.name': 'Test University', 'school.city': 'Boston', 'school.state': 'Massachusetts',
                      '2018.student.size': 1000, '2017.student.size': 900,
                      '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                      '2016.repayment.3_yr_repayment.overall': 4004,
                      '2016.repayment.repayment_cohort.3_year_declining_balance': 2000}]

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
