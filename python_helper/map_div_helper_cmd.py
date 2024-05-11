import os
import subprocess

from tqdm import tqdm

current_script_path = os.path.dirname(os.path.abspath(__file__))
pointcloud_map_divider_path = os.path.join(current_script_path,
                                           "pointcloud_divider")  # https://github.com/MapIV/pointcloud_divider自己编译一下个 或者用我编译好的 pointcloud_divider
CONFIG_FILE = os.path.join(current_script_path, "divider_cfg.yaml")
PREFIX = "pointcloud_map"  # 这个是启动文件默认用的前缀

if __name__ == '__main__':
    # 需要 6个参数  $N_PCD $PCD_FILES $OUTPUT_DIR $PREFIX $CONFIG_FILE

    # 保存的pcd的文件夹
    pcd_file_dir_list = [
        os.path.abspath(os.path.join(current_script_path, "..", "map_data")),
        '/home/jimmy/ros_dev/zj_atv_ws/src/beamng_autoware/config/map/west_cost_dynamic/pointcloud_map',
    ]

    # search all *.pcd files in the directory recursively
    PCD_FILES = []
    for pcd_file_dir in pcd_file_dir_list:
        for root, dirs, files in os.walk(pcd_file_dir):
            for file in files:
                if file.endswith(".pcd"):
                    PCD_FILES.append(os.path.join(root, file))

    N_PCD = len(PCD_FILES)

    print(f"Found {N_PCD} pcd files")

    OUTPUT_DIR = os.path.abspath(os.path.join(current_script_path, "result", "map"))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    map_divider_cmd = [
        pointcloud_map_divider_path,
        N_PCD,
        *PCD_FILES,
        OUTPUT_DIR,  # 有点煞笔。这个输出目录是这个地址的父目录
        PREFIX,
        CONFIG_FILE,
    ]
    # str map_divider_cmd
    map_divider_cmd = list(map(str, map_divider_cmd))

    print("cmd:", " ".join(map_divider_cmd))

    # subprocess.run(map_divider_cmd)

    pbar = tqdm(total=N_PCD)

    proc = subprocess.Popen(map_divider_cmd,
                            stdout=subprocess.PIPE,
                            # stderr=subprocess.PIPE
                            )

    for line in iter(proc.stdout.readline, b''):
        l = line.decode().strip()
        if l in PCD_FILES:
            pbar.update(1)
        # pbar.update(1)
    pbar.update(1)
    pbar.close()

    # # print all stderr
    # print("stderr: ")
    # for line in iter(proc.stderr.readline, b''):
    #     l = line.decode().strip()
    #     print(l)

    proc.wait()
