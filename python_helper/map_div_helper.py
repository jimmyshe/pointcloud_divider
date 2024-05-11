import os
import typing

from PyQt5.QtCore import QProcess, pyqtSignal
import logging
import yaml


def create_temp_yaml_cfg(cfg: dict):
    cfg_path = '/tmp/pointcloud_divider_cfg.yaml'
    with open(cfg_path, 'w') as f:
        yaml.dump(cfg, f)
    return cfg_path


class PointCloudDividerProcess(QProcess):
    progress_signal = pyqtSignal(int, int)  # finished, total
    error_msg_signal = pyqtSignal(str)
    std_msg_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.readyReadStandardOutput.connect(self.handle_stdout)
        self.readyReadStandardError.connect(self.handle_stderr)

        self.to_do_list = []
        self.finished_count = 0

    def is_busy(self):
        return self.state() == QProcess.Running

    def _form_args(self, input_files: typing.List[str], output_folder: str, cfg, prefix="pointcloud_map"):
        # search all *.pcd files in the directory recursively
        CONFIG_FILE = create_temp_yaml_cfg(cfg)
        PREFIX = prefix  # 这个是启动文件默认用的前缀
        PCD_FILES = input_files
        N_PCD = len(PCD_FILES)
        OUTPUT_DIR = os.path.abspath(output_folder)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        map_divider_args = [
            N_PCD,
            *PCD_FILES,
            OUTPUT_DIR,  # 有点煞笔。这个输出目录是这个地址的父目录
            PREFIX,
            CONFIG_FILE,
        ]
        # str map_divider_cmd
        map_divider_args = list(map(str, map_divider_args))
        return map_divider_args, PCD_FILES

    def start_div(self, input_files, output_folder, cfg):
        pointcloud_map_divider_path = '/home/jimmy/CLionProjects/ag/pointcloud_divider/cmake-build-release/pointcloud_divider'
        args, self.to_do_list = self._form_args(input_files, output_folder, cfg)
        logging.info(f"Start dividing pointclouds: {args}")
        super().start(pointcloud_map_divider_path, args)

    def cancel(self):
        self.to_do_list = []
        self.finished_count = 0
        self.kill()

    def handle_stdout(self):
        data = self.readAllStandardOutput().data().decode()
        self.std_msg_signal.emit(data)
        data = data.strip()
        if data in self.to_do_list:
            self.finished_count += 1
            self.progress_signal.emit(self.finished_count, len(self.to_do_list))

    def handle_stderr(self):
        data = self.readAllStandardError().data().decode()
        self.error_msg_signal.emit(data)
