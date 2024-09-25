import warnings
import _tanway
from tanway.point_cloud import PointCloud
from tanway.device_info import DeviceInfo

class Lidar:
    def __init__(self):
        self.__impl = _tanway.LidarDevice()
        self.lidar_types = {
            "Tensor16": 0,
            "Tensor32": 1,
            "Scope192": 2,
            "Duetto": 3,
            "TempoA1": 4,
            "TempoA2": 5,
            "ScopeMini":6,
            "TempoA3": 7,
            "TempoA4": 8,
            "Tensor48": 9,
            "Tensor48_Depth": 10,
            "Scope256": 11,
            "Scope256_Depth": 12,
            "FocusB1": 13,
            "Scope256_SmallBlind": 14,
            "FocusB2": 15,
            "Scope128": 17,
            "Scope128F": 18
        }

    def __str__(self):
        return str(self.__impl)
    
    def create_offline(self, pcapPath, lidarIPForFilter, pointloudPort, DIFPort, lidarType, repeat):
        warnings.warn("Use create function instead!", DeprecationWarning)
        try:
            lidar_type_class = self.lidar_types[lidarType]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {lidar_type}. Supported formats: {all_formats}".format(
                    lidar_type=lidarType, all_formats=list(self.lidar_types.keys())
                )
            ) from ex
        
        return self.__impl.create(pcapPath, lidarIPForFilter, pointloudPort, DIFPort, lidar_type_class)
    
    def create_online(self, lidarIP, hostIP, pointloudPort, DIFPort, lidarType):
        warnings.warn("Use create function instead!", DeprecationWarning)
        try:
            lidar_type_class = self.lidar_types[lidarType]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {lidar_type}. Supported formats: {all_formats}".format(
                    lidar_type=lidarType, all_formats=list(self.lidar_types.keys())
                )
            ) from ex
        
        return self.__impl.create(lidarIP, hostIP, pointloudPort, DIFPort, lidar_type_class)

    def create(self, lidarIPOrPcapPath, hostIPOrLidarIPForFilter, pointloudPort, DIFPort, lidarType):
        try:
            lidar_type_class = self.lidar_types[lidarType]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {lidar_type}. Supported formats: {all_formats}".format(
                    lidar_type=lidarType, all_formats=list(self.lidar_types.keys())
                )
            ) from ex
        
        return self.__impl.create(lidarIPOrPcapPath, hostIPOrLidarIPForFilter, pointloudPort, DIFPort, lidar_type_class)
    
    def start(self):
        return self.__impl.start()
    
    def stop(self):
        return self.__impl.stop()
    
    def parse_pcap(self):
        return self.__impl.parse_pcap()

    def seek(self, index):
        return self.__impl.seek(index)

    def eof(self):
        return self.__impl.eof()

    def capture(self):
        return PointCloud(self.__impl.capture())

    def device_info(self):
        return DeviceInfo(self.__impl.device_info())

    def get_total_frames(self):
        return self.__impl.get_total_frames()

    def set_distance_range(self, min, max):
        return self.__impl.set_distance_range(min, max)
    
    def set_angle_range(self, min, max):
        return self.__impl.set_angle_range(min, max)

    def set_echo_num(self, echo):
        data_formats = {
            "one": 0x01,
            "two": 0x02,
            "both": 0x03,
        }
        try:
            data_format_class = data_formats[echo]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {data_format}. Supported formats: {all_formats}".format(
                    data_format=echo, all_formats=list(data_formats.keys())
                )
            ) from ex
        return self.__impl.set_echo_num(data_format_class)

    def set_mirror_vertical_angle_offset(self, a, b, c):
        return self.__impl.set_mirror_vertical_angle_offset(a, b, c)

    def set_play_rate(self, rate):
        return self.__impl.set_play_rate(rate)

    def parse_algo_config(self, algo_config):
        return self.__impl.parse_algo_config(algo_config)