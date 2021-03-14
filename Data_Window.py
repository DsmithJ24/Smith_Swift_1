from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem
from typing import List, Dict


class SearchWindow(QWidget):
    def __init__(self, main_self):
        super().__init__()
        self.from_main = main_self
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Select Data")
        self.setGeometry(150, 150, 300, 200)

        quit_button = QPushButton("Exit", self)
        quit_button.clicked.connect(self.close)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(100, 150)

        # ToDo: rename this later to search, there will be no default
        default_button = QPushButton("Use Default", self)
        default_button.resize(default_button.sizeHint())
        default_button.move(200, 150)
        default_button.clicked.connect(self.show_message)
        self.show()

    def show_message(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Message")
        message_box.setText("Default Selected!!!")
        '''
        message_box.setStandardButtons(QMessageBox.Ok)
        return_value = message_box.exec_()
        if return_value == QMessageBox.Ok:
            self.use_default()
        '''
        message_box.show() # shows the message box itself
    '''
    def use_default(self):
        MainWindow.show_data(self.from_main)
        self.close()
    '''

class MainWindow(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.data = data_to_show
        self.list_control = None
        self.reference_window = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Data_Window")

        # ToDo: next few lines should be done once data has been chosen
        display_list = QListWidget(self)

        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)

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
            display_item = f"{item['total students']}\t\t{item['3 year balance']}\t\t{item['occ_code']}" \
                           f"\t\t{item['hourly salary']}"
            list_item = QListWidgetItem(display_item, listview=self.list_control)

    def update_data(self):
        # ToDO: figure out how to make a second regular GUI pop up, not a message box
        if self.reference_window is None:
            self.reference_window = SearchWindow(self)
            self.reference_window.show()
        else:
            self.reference_window.close()
            self.reference_window = None
            #self.show_data()

        # ToDO: when updating the data, take a user input for a file. Bring up GUI that has either default button
        #  or search bar with search button
    '''
    def show_data(self):
        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)
        self.show()
    '''
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
