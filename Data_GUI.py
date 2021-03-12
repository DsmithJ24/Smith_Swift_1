import openpyxl
import PySide6.QtWidgets
import sys
import Data_Window
import numbers
from typing import List, Dict


def display_data(data: list):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)
    my_window = Data_Window.SprintWindow(data)
    sys.exit(qt_app.exec_())


def get_data() -> List[Dict]:

    # ToDO later in project, make it so the wb name is a variable that takes an input
    workbook_file = openpyxl.load_workbook("state_M2019_dl.xlsx")
    worksheet = workbook_file.active
    data_list = []
    for current_row in worksheet.rows:
        state_cell = current_row[0]
        state_name = state_cell.value
        median_income2018 = current_row[1].value
        if not isinstance(median_income2018, numbers.Number):
            continue
        record = {"state_name": state_name, "median_income": median_income2018}
        data_list.append(record)
    return data_list


def get_key(value:dict):
    return value["median_income"]


# ToDo: next two funcs may be changed and/or put in Data.py
def main():
    data = get_data()
    data.sort(key=get_data)
    display_data(data)


if __name__ == '__main__':
    main()
