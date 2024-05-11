import os
import typing

from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QPushButton, QWidget


class DirectoryPicker(QWidget):
    def __init__(self, dir_key_name=''):
        super().__init__()
        self.dir_key_name = dir_key_name
        self.initUI()
        self.button.clicked.connect(self.getDirectoryFromDialog)

        self.dir = None

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.dir_label = QLabel('No directory selected')
        layout.addWidget(self.dir_label)

        self.button = QPushButton('Choose Directory')
        layout.addWidget(self.button)

    def setDirectory(self, dir_path):
        self.dir = dir_path
        self.dir_label.setText(f'Selected {self.dir_key_name} Directory: {dir_path}')

    def getDirectory(self) -> typing.Optional[str]:
        if self.dir is None:
            return None
        if not os.path.exists(self.dir):
            return None
        else:
            return self.dir

    def getDirectoryFromDialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, f'Select {self.dir_label} Directory')
        self.setDirectory(dir_path)
