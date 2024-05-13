from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget
from map_div_gui import PointCloudDivider
from pcd_coordinate_convert_gui import CloudCoordinateConverter


class TabbedFileListManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)

        self.pointCloudDivider = PointCloudDivider()
        self.tabWidget.addTab(self.pointCloudDivider, "PointCloudDivider")

        self.cloudCoordinateConverter = CloudCoordinateConverter()
        self.tabWidget.addTab(self.cloudCoordinateConverter, "CloudCoordinateConverter")



if __name__ == '__main__':
    app = QApplication([])
    demo = TabbedFileListManager()
    demo.show()
    app.exec_()
