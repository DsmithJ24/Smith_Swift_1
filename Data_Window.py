from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem
from typing import List, Dict


class SprintWindow(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.data = data_to_show
        self.list_control = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Data_Window")
        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)
        self.setGeometry(100, 100, 400, 500)

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
            display_item = f"{item['state_name']}\t\t{item['median_income']}"
            list_item = QListWidgetItem(display_item, listview=self.list_control)

    def update_data(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Message")
        message_box.setText("Data has been updated!")
        message_box.show()

    def data_visualization(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Message")
        message_box.setText("Visualization complete!")
        message_box.show()
