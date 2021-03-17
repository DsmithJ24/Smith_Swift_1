from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QLineEdit, \
    QLabel
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
        # ToDo: do the get data func in Data_GUI and pass in the file name
        MainWindow.show_data(self.from_main)
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
    #def __init__(self, data_to_show):
    def __init__(self):
        super().__init__()
        self.data = None
        self.list_control = None
        self.reference_window = None
        self.setup_window()
        self.display_list = None

    def setup_window(self):
        self.setWindowTitle("Data_Window")
        self.setGeometry(100, 100, 600, 500)
        quit_button = QPushButton("Exit", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(300, 400)

        update_data_button = QPushButton("Update Data", self)
        update_data_button.resize(update_data_button.sizeHint())
        update_data_button.move(50, 400)
        update_data_button.clicked.connect(self.update_data)

        run_visualization = QPushButton("Data Visualization", self)
        run_visualization.resize(run_visualization.sizeHint())
        run_visualization.move(150, 400)
        run_visualization.clicked.connect(self.data_visualization)
        self.show()

    def put_data_in_list(self, data: List[Dict]):
        for item in data:
            display_item1 = f"{item['total students']}\t\t{item['3 year balance']}\t\t{item['occ_code']}" \
                            f"\t\t{item['hourly salary']}"
            list_item1 = QListWidgetItem(display_item1, listview=self.list_control)

    def update_data(self):
        if self.reference_window is None:
            self.reference_window = SearchWindow(self)
            self.reference_window.show()
        else:
            self.reference_window.close()
            self.reference_window = None

    def show_data(self):
        self.data = Data_GUI.display_data()
        self.display_list = QListWidget(self)
        self.list_control = self.display_list
        self.put_data_in_list(self.data)
        self.display_list.resize(400, 350)
        self.display_list.show() # show this widget, not the whole thing

    def data_visualization(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Message")
        message_box.setText("Visualization complete!")
        message_box.show()

    # ToDO: Create a GUI for the data
    #  GUI should allow user to update the data or visualize data

    # ToDo: For visualization, have two forms of data analysis
    #  1) display data in color coded text format as a list in ascending or descending order (user chooses)
    #  2) render a map to visualize data
