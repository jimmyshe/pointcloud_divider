import datetime
import logging
import os

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QProgressBar,
    QPlainTextEdit, QSizePolicy,
)
from map_div_helper import PointCloudDividerProcess
from file_list_widget import FileListManager
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget

from dir_picker import DirectoryPicker
from cfg_editor import ConfigEditor


class PointCloudDivider(QWidget):
    def __init__(self):
        super().__init__()

        # Variables
        self.output_folder = None
        self.initUI()

        self.input_file_manager.add_init_files([
            '/home/jimmy/ros_dev/zj_atv_ws/src/beamng_autoware/config/map/west_cost_dynamic/pointcloud_map/pointcloud_map_00000.pcd',
        ])

        # set a default out folder
        test_dir = os.path.abspath('test_dir')
        if os.path.exists(test_dir):
            self.output_folder_picker.setDirectory(test_dir)

        self.worker = PointCloudDividerProcess()
        # connect signals of worker
        self.worker.progress_signal.connect(self.handle_progress)
        self.worker.started.connect(self.handle_start)
        self.worker.finished.connect(self.handle_finish)

        self.worker.error_msg_signal.connect(self.logtext.appendPlainText)
        self.worker.std_msg_signal.connect(self.logtext.appendPlainText)

        # connect signals of buttons
        self.cancel_button.clicked.connect(self.worker.cancel)
        self.run_button.clicked.connect(self.run)

    def initUI(self):
        self.setWindowTitle('PointCloudDivider')
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_file_manager = FileListManager()
        layout.addWidget(self.input_file_manager)

        self.output_folder_picker = DirectoryPicker('Output')
        layout.addWidget(self.output_folder_picker)

        self.config_editor = ConfigEditor()
        layout.addWidget(self.config_editor)

        self.logtext = QPlainTextEdit()
        self.logtext.setReadOnly(True)
        layout.addWidget(self.logtext)

        control_layout = QHBoxLayout()
        layout.addLayout(control_layout)

        # run button
        self.run_button = QPushButton('Run')
        control_layout.addWidget(self.run_button)

        # cancel button
        self.cancel_button = QPushButton('Cancel')
        control_layout.addWidget(self.cancel_button)

        # progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

    def handle_progress(self, finished, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(finished)

    def handle_start(self):
        logging.info('Start running...')
        self.run_button.setText('Running...')
        self.run_button.setEnabled(False)
        self.logtext.appendPlainText('Start running...')

    def handle_finish(self):
        logging.info('Finished.')
        self.run_button.setText('Run')
        self.run_button.setEnabled(True)
        self.handle_progress(0, 1)

    def run(self):
        if self.worker.is_busy():
            QMessageBox.warning(self, 'Warning', 'The worker is running, please wait until it finishes.')

        self.logtext.clear()

        input_files = self.input_file_manager.get_files()
        if len(input_files) == 0:
            QMessageBox.warning(self, 'Warning', 'Please add input files first.')
            return

        output_folder = self.output_folder_picker.getDirectory()

        if output_folder is None:
            QMessageBox.warning(self, 'Warning', 'Please choose output folder first.')
            return

        if not os.path.exists(output_folder):
            QMessageBox.warning(self, 'Warning', 'The output folder is not exist. Please choose another one.')
            return

        cfg = self.config_editor.get_config()

        self.logtext.appendPlainText(f"{datetime.datetime.now()} use config: {cfg}")

        self.worker.start_div(input_files, output_folder, cfg)


if __name__ == '__main__':
    app = QApplication([])
    demo = PointCloudDivider()
    demo.show()
    app.exec_()
