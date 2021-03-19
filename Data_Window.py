from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, \
    QLineEdit, QLabel, QTableWidget, QTableWidgetItem
from typing import List, Dict
import Data_GUI


class SearchWindow(QWidget):
    def __init__(self, main_self):
        super().__init__()
        self.from_main = main_self
        self.setup_window()
        self.file_name = ""
        self.message_to_user = None

    def setup_window(self):
        self.setWindowTitle("Select Data")
        self.setGeometry(150, 150, 300, 100)
        self.message_to_user = QLabel("Please enter a file name", self)
        self.message_to_user.move(25, 15)
        search_bar = QLineEdit(self)
        search_bar.resize(250, 25)
        search_bar.move(25, 35)
        search_bar.textChanged.connect(self.save_file_name)

        quit_button = QPushButton("Exit", self)
        quit_button.clicked.connect(self.close)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(100, 70)

        default_button = QPushButton("Search", self)
        default_button.resize(default_button.sizeHint())
        default_button.move(200, 70)
        default_button.clicked.connect(self.find_file)
        self.show()

    def save_file_name(self, text):
        self.file_name = text

    def find_file(self):
        if Data_GUI.find_file(self.file_name) is True:
            self.show_good_message()
        else:
            self.show_error_message()

    def show_good_message(self):
        Data_GUI.initialize_db(self.file_name)
        MainWindow.get_data(self.from_main, self.file_name)
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Success")
        message_box.setText("Data Retrieved.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.show()  # shows the message box itself
        self.close()

    def show_error_message(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Failure")
        message_box.setText("File does not exist. Please enter a different file name.")
        message_box.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.job_data = None
        self.repayment_data = None
        self.list_control = None
        self.reference_window = None
        self.setup_window()
        self.display_list = None

    def setup_window(self):
        self.setWindowTitle("Data_Window")
        self.setGeometry(100, 100, 600, 550)
        quit_button = QPushButton("Exit", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(500, 500)

        update_data_button = QPushButton("Update Data", self)
        update_data_button.resize(update_data_button.sizeHint())
        update_data_button.move(50, 500)
        update_data_button.clicked.connect(self.update_data)

        run_job_visualization = QPushButton("Job Visualization", self)
        run_job_visualization.resize(run_job_visualization.sizeHint())
        run_job_visualization.move(150, 500)
        run_job_visualization.clicked.connect(self.data_visualization_jobs)

        run_repayment_visualization = QPushButton("Repayment Visualization", self)
        run_repayment_visualization.resize(run_repayment_visualization.sizeHint())
        run_repayment_visualization.move(300, 500)
        run_repayment_visualization.clicked.connect(self.data_visualization_repayment)

        increasing_job_button = QPushButton("Order by Ascending Job Numbers", self)
        increasing_job_button.resize(increasing_job_button.sizeHint())
        increasing_job_button.move(100, 400)
        increasing_job_button.clicked.connect(self.increasing_order_job)

        decreasing_job_button = QPushButton("Order by Descending Job Numbers", self)
        decreasing_job_button.resize(decreasing_job_button.sizeHint())
        decreasing_job_button.move(300, 400)
        decreasing_job_button.clicked.connect(self.decreasing_order_job)

        increasing_repayment_button = QPushButton("Order by Ascending Repayment Numbers", self)
        increasing_repayment_button.resize(increasing_repayment_button.sizeHint())
        increasing_repayment_button.move(50, 450)
        increasing_repayment_button.clicked.connect(self.increasing_order_repayment)

        decreasing_repayment_button = QPushButton("Order by Descending Repayment Numbers", self)
        decreasing_repayment_button.resize(decreasing_repayment_button.sizeHint())
        decreasing_repayment_button.move(300, 450)
        decreasing_repayment_button.clicked.connect(self.decreasing_order_repayment)
        self.show()

    def put_job_data_in_gui(self, data: List[Dict]):
        data_index = 0

        for item in data:
            display_item = f"{item['state']}\t\t{item['graduates']}\t\t{item['jobs']}\t\t{item['jobs_vs_graduates']}"
            list_item = QListWidgetItem(display_item, listview=self.list_control)
            self.color_data(list_item, data_index)
            data_index = data_index + 1

    def put_repayment_data_in_gui(self, data: List[Dict]):
        data_index = 0
        for item in data:
            display_item = f"{item['state']}\t\t{item['school_name']}\t\t{item['job_title']}" \
                           f"\t\t{item['bad_repayment_odds']}"
            list_item = QListWidgetItem(display_item, listview=self.list_control)
            self.color_data(list_item, data_index)
            data_index = data_index + 1

    def update_data(self):
        if self.reference_window is None:
            self.reference_window = SearchWindow(self)
            self.reference_window.show()
        else:
            self.reference_window.close()
            self.reference_window = None

    def get_data(self, file_name):
        self.job_data, self.repayment_data = Data_GUI.display_data('sprint_db.sqlite')

    def data_visualization_jobs(self):
        if self.job_data is None:
            self.show_error_message("No data Available. Please update data!")

        else:
            self.put_in_QList()
            self.put_job_data_in_gui(self.job_data)
            self.display_list.resize(600, 350)
            self.display_list.show() # show this widget, not the whole thing

    def data_visualization_repayment(self):
        print(self.repayment_data)
        if self.repayment_data is None:
            self.show_error_message("No data Available. Please update data!")

        else:
            self.put_in_QList()
            self.put_repayment_data_in_gui(self.repayment_data)
            self.display_list.resize(600, 350)
            self.display_list.show() # show this widget, not the whole thing

    def put_in_QList(self):
        self.display_list = QListWidget(self)
        self.list_control = self.display_list

    def show_error_message(self, error_message: str):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Error")
        message_box.setText(error_message)
        message_box.show()

    # def color_data(self, entry: QListWidgetItem, entry_number: int):
    def color_data(self, entry: QListWidgetItem, entry_number: int):
        colors = ["red", "blue", "orange", "green", "pink", "yellow", "purple", "brown", "gray", "black"]
        end_digit = entry_number % 10
        entry.setForeground(QBrush(QColor(colors[end_digit])))

    def increasing_order_job(self):
        if self.job_data is None:
            self.show_error_message("No data Available. Please update data!")

        elif self.display_list is None:
            self.show_error_message("Please visualize the data first!")

        else:
            self.job_data = Data_GUI.sort_jobs_increasing(self.job_data)
            self.data_visualization_jobs()

    def increasing_order_repayment(self):
        if self.repayment_data is None:
            self.show_error_message("No data Available. Please update data!")

        elif self.display_list is None:
            self.show_error_message("Please visualize the data first!")

        else:
            self.repayment_data = Data_GUI.sort_repayment_increasing(self.repayment_data)
            self.data_visualization_repayment()

    def decreasing_order_job(self):
        if self.job_data is None:
            self.show_error_message("No data Available. Please update data!")

        elif self.display_list is None:
            self.show_error_message("Please visualize the data first!")

        else:
            self.job_data = Data_GUI.sort_jobs_decreasing(self.job_data)
            self.data_visualization_jobs()

    def decreasing_order_repayment(self):
        if self.repayment_data is None:
            self.show_error_message("No data Available. Please update data!")

        elif self.display_list is None:
            self.show_error_message("Please visualize the data first!")

        else:
            self.repayment_data = Data_GUI.sort_repayment_decreasing(self.repayment_data)
            self.data_visualization_repayment()

    # ToDo: For visualization, have two forms of data analysis
    #  2) render a map to visualize data
