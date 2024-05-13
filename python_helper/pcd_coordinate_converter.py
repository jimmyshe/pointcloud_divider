from pypcd4 import Encoding, PointCloud

from pyproj import CRS, Transformer


def convert_mgrs_to_utm_info(mgrs_code):
    # Define the MGRS and UTM coordinate systems
    # mgrs_crs = CRS.from_string("EPSG:4326")
    # utm_crs = CRS.from_epsg(32632)  # This is for UTM zone 32N. Change it according to your needs.
    #
    # # Create a transformer to convert from MGRS to UTM
    # transformer = Transformer.from_crs(mgrs_crs, utm_crs)
    #
    # # Split the MGRS code into its components
    # zone, latitude_band, easting, northing = mgrs_code[:2], mgrs_code[2], mgrs_code[3:8], mgrs_code[8:]
    #
    # # Convert the MGRS coordinates to UTM coordinates
    # utm_easting, utm_northing = transformer.transform(easting, northing)

    zone = mgrs_code[:2]
    latitude_band = mgrs_code[2]
    if 'A' <= latitude_band <= 'M' and latitude_band not in ['I', 'O']:
        hemisphere = 'S'
    elif 'N' <= latitude_band <= 'Z' and latitude_band != 'O':
        hemisphere = 'N'

    square_id = mgrs_code[3:5]


    return zone, hemisphere, utm_easting, utm_northing


def convert_mgrs_to_utm(mgrs_code, mgrs_cloud_path, output_dir):
    utm_zone, hemisphere, x_origin, y_origin = convert_mgrs_to_utm_info(mgrs_code)

    print(utm_zone, hemisphere, x_origin, y_origin)

    # cloud = PointCloud.from_path(mgrs_cloud_path)
    # pointXYZ = cloud.numpy(["x", "y", "z"])
    #
    # # convert the point cloud to utm
    # pointXYZ[:, 0] += x_origin
    # pointXYZ[:, 1] += y_origin
    #
    # utm_cloud = PointCloud.from_xyz_points(pointXYZ)
    #
    # # get_file_name without extension from path
    # file_name = mgrs_cloud_path.split("/")[-1].split(".")[0]
    #
    # out_file_name_no_extension = f"{output_dir}/{file_name}_{utm_zone}{hemisphere}"
    # # save the pcd
    # utm_cloud.save(f"{out_file_name_no_extension}.pcd",
    #                encoding=Encoding.ASCII)
    #
    # # save as ply
    # import laspy
    # las = laspy.create(point_format=2)
    # las.x = pointXYZ[:, 0]
    # las.y = pointXYZ[:, 1]
    # las.z = pointXYZ[:, 2]
    # las.write(f"{out_file_name_no_extension}.las")


if __name__ == '__main__':
    # load pcd
    pcd_file_path = "/home/jimmy/Documents/zj_map/pointcloud_map.pcd"
    mgrs_pcd = "49QDD"
    output_dir = "/home/jimmy/Documents/zj_map"

    convert_mgrs_to_utm(mgrs_pcd, pcd_file_path, output_dir)
