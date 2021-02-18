import Data

DATA_MINIMUM = 1000

def test_data_entries():
    data = Data.get_data()
    assert len(data) <= DATA_MINIMUM


def test_store_data():
    conn, cursor = Data.open_DB("demo_db.sqlite")
    Data.setup_DB(cursor)

    data = Data.get_data()
    Data.store_In_DB(data, cursor)

    Data.close_DB(conn)
