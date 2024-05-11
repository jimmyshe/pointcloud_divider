import os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QListWidget, QFileDialog
import fnmatch


class FileListManager(QWidget):
    def __init__(self, file_filter="*.pcd"):
        super().__init__()
        self.file_filter = file_filter
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.listWidget = QListWidget()
        layout.addWidget(self.listWidget)

        control_layout = QVBoxLayout()
        layout.addLayout(control_layout)

        self.addButton = QPushButton('Add Files')
        self.addButton.clicked.connect(self.add_files)
        control_layout.addWidget(self.addButton)

        self.add_dir_button = QPushButton('Add Directory')
        self.add_dir_button.clicked.connect(self.add_directory)
        control_layout.addWidget(self.add_dir_button)

        control_layout.addStretch(1)

        self.deleteButton = QPushButton('Delete Selected File')
        self.deleteButton.clicked.connect(self.delete_file)
        control_layout.addWidget(self.deleteButton)

        self.clearButton = QPushButton('Clear All')
        self.clearButton.clicked.connect(self.listWidget.clear)
        control_layout.addWidget(self.clearButton)

    def get_files(self):
        return [self.listWidget.item(i).text() for i in range(self.listWidget.count())]

    def add_files(self):
        files_path, _ = QFileDialog.getOpenFileNames(self, 'Select File', filter=self.file_filter)
        for file_path in files_path:
            self.listWidget.addItem(file_path)

    def add_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        # walk through the directory and add all files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if fnmatch.fnmatch(file, self.file_filter):
                    self.listWidget.addItem(os.path.join(root, file))

    def delete_file(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))


if __name__ == '__main__':
    app = QApplication([])
    demo = FileListManager()
    demo.show()
    app.exec_()
