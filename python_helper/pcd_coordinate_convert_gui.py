import logging

from PyQt5.QtWidgets import QApplication, QFormLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit, QPushButton, \
    QVBoxLayout, QWidget

from dir_picker import DirectoryPicker
from file_list_widget import FileListManager
from pcd_coordinate_converter import convert_mgrs_to_utm


class CloudCoordinateConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.start_button.clicked.connect(self.start_convert)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fileListManager = FileListManager()
        layout.addWidget(self.fileListManager)

        self.out_dir_edit = DirectoryPicker("Output Directory")
        layout.addWidget(self.out_dir_edit)

        code_settings_layout = QFormLayout()
        layout.addLayout(code_settings_layout)


        self.logtext = QPlainTextEdit()
        self.logtext.setReadOnly(True)
        layout.addWidget(self.logtext)

        # MGRS code settings
        self.mgrs_code_edit = QLineEdit()
        self.mgrs_code_edit.setText("49QDD")  # default value
        code_settings_layout.addRow(QLabel("MGRS Code"), self.mgrs_code_edit)

        # # UTM zone settings
        # self.utm_zone_edit = QLineEdit()
        # code_settings_layout.addRow(QLabel("UTM Zone"), self.utm_zone_edit)

        self.start_button = QPushButton("mgrs to utm")
        layout.addWidget(self.start_button)

    def start_convert(self):
        logging.info("Start converting")

        mgrs_code = self.mgrs_code_edit.text()

        input_files = self.fileListManager.get_files()
        output_dir = self.out_dir_edit.get_directory()

        if len(input_files) == 0:
            QMessageBox.warning(self, 'Warning', 'No input files selected', QMessageBox.Ok)
            return

        if not output_dir:
            QMessageBox.warning(self, 'Warning', 'No output directory selected', QMessageBox.Ok)
            return

        for file in input_files:
            convert_mgrs_to_utm(mgrs_code, file, output_dir)

        logging.info("Finished converting")


if __name__ == '__main__':
    app = QApplication([])
    demo = CloudCoordinateConverter()
    demo.show()
    app.exec_()
