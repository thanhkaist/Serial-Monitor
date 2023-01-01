import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton, QWidget)

class TextFilterVisualization(QWidget):
    def __init__(self):
        super().__init__()

        # Create the QLineEdit and QListWidget widgets
        self.filter_input = QLineEdit()
        self.filter_list = QListWidget()

        # Create the "Add", "Remove", and "Clear" buttons
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear")

        # Connect the "Add" button's clicked signal to the add_filter_item slot
        self.add_button.clicked.connect(self.add_filter_item)

        # Connect the "Remove" button's clicked signal to the remove_filter_item slot
        self.remove_button.clicked.connect(self.remove_filter_item)

        # Connect the "Clear" button's clicked signal to the clear_filter_list slot
        self.clear_button.clicked.connect(self.clear_filter_list)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Filter:"), 0, 0)
        layout.addWidget(self.filter_input, 0, 1)
        layout.addWidget(self.add_button, 0, 2)
        layout.addWidget(QLabel("Filter Items:"), 1, 0)
        layout.addWidget(self.filter_list, 2, 0, 1, 3)
        layout.addWidget(self.remove_button, 3, 0)
        layout.addWidget(self.clear_button, 3, 2)

        # Create a central widget and set its layout
        
        self.setLayout(layout)

    def add_filter_item(self):
        # Get the text from the QLineEdit widget
        filter_text = self.filter_input.text()

        # Add the text to the QListWidget
        self.filter_list.addItem(filter_text)

        # Clear the QLineEdit
        self.filter_input.clear()

    def remove_filter_item(self):
        # Get the selected items from the QListWidget
        selected_items = self.filter_list.selectedItems()

        # If there are any selected items, remove them from the QListWidget
        if selected_items:
            for item in selected_items:
                self.filter_list.takeItem(self.filter_list.row(item))

    def clear_filter_list(self):
        # Clear the QListWidget
        self.filter_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextFilterVisualization()
    window.show()
    sys.exit(app.exec_())