from PyQt5.QtWidgets import QApplication, QCheckBox, QDoubleSpinBox, QSlider, QVBoxLayout, QPushButton, QWidget, QLabel, \
    QLineEdit, \
    QFormLayout


class ConfigEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.formLayout = QFormLayout()
        layout.addLayout(self.formLayout)

        self.use_large_grid_checkbox = QCheckBox()
        self.use_large_grid_checkbox.setChecked(True)
        self.formLayout.addRow(QLabel('use_large_grid'), self.use_large_grid_checkbox)

        self.merge_pcds_checkbox = QCheckBox()
        self.merge_pcds_checkbox.setChecked(False)
        self.formLayout.addRow(QLabel('merge_pcds'), self.merge_pcds_checkbox)

        self.leaf_size_slider = QDoubleSpinBox()
        self.leaf_size_slider.setRange(0.01, 2)
        self.leaf_size_slider.setValue(0.1)
        self.leaf_size_slider.setSingleStep(0.01)
        self.formLayout.addRow(QLabel('leaf_size'), self.leaf_size_slider)

        self.grid_size_x_slider = QDoubleSpinBox()
        self.grid_size_x_slider.setRange(10.0, 100.0)
        self.grid_size_x_slider.setValue(20)
        self.grid_size_x_slider.setSingleStep(1)
        self.formLayout.addRow(QLabel('grid_size_x'), self.grid_size_x_slider)
        #
        self.grid_size_y_slider = QDoubleSpinBox()
        self.grid_size_y_slider.setRange(10.0, 100.0)
        self.grid_size_y_slider.setValue(20)
        self.grid_size_y_slider.setSingleStep(1)
        self.formLayout.addRow(QLabel('grid_size_y'), self.grid_size_y_slider)

    def get_config(self):
        use_large_grid = self.use_large_grid_checkbox.isChecked()
        merge_pcds = self.merge_pcds_checkbox.isChecked()
        leaf_size = self.leaf_size_slider.value()
        grid_size_x = self.grid_size_x_slider.value()
        grid_size_y = self.grid_size_y_slider.value()

        return {
            "pointcloud_divider": {
                "use_large_grid": use_large_grid,
                "merge_pcds": merge_pcds,
                "leaf_size": leaf_size,
                "grid_size_x": grid_size_x,
                "grid_size_y": grid_size_y,
            }
        }


if __name__ == '__main__':
    app = QApplication([])
    demo = ConfigEditor()
    demo.show()
    app.exec_()
