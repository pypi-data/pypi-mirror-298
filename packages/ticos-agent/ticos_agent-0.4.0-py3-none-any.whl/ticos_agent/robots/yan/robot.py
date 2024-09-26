from abc import ABC, abstractmethod
import os


class DeviceInterface(ABC):
    @abstractmethod
    def get_device_info(self):
        pass

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def execute_command(self, command_name, **kwargs):
        pass


try:
    import YanAPI
except ImportError:
    print("Warning: YanAPI is not installed. Some functionality may be limited.")
    YanAPI = None


class YanRobot(DeviceInterface):
    def __init__(self):
        if YanAPI is None:
            raise ImportError("YanAPI is not installed. Install it to use YanRobot.")
        self.ip_addr = os.environ.get("YANSHEE_IP", "127.0.0.1")
        self.initialize_api()

    def initialize_api(self):
        YanAPI.yan_api_init(self.ip_addr)

    def get_device_info(self):
        return "YanRobot"

    def collect_data(self):
        volume = YanAPI.get_robot_volume()
        battery = YanAPI.get_robot_battery_info()
        return {
            "volume": volume["data"]["volume"],
            "battery_percent": battery["data"]["percent"],
            "battery_charging": battery["data"]["charging"],
            "battery_voltage": battery["data"]["voltage"],
        }

    def execute_command(self, command_name, **kwargs):
        if command_name == "start_video_stream":
            return self._start_video_stream()
        else:
            return {
                "success": False,
                "message": "Unknown command: {}".format(command_name),
            }

    def _start_video_stream(self):
        try:
            api_instance = YanAPI.VisionsApi()
            api_response = api_instance.post_visions_streams()
            return {
                "success": True,
                "message": "Video stream started. Access at http://{}:8000".format(
                    self.ip_addr
                ),
                "data": api_response,
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to start video stream: {}".format(str(e)),
                "error": str(e),
            }


# Test function
def test_yan_robot():
    try:
        robot = YanRobot()
        print("YanRobot initialized successfully.")

        print("\nTesting get_device_info:")
        print(robot.get_device_info())

        print("\nTesting collect_data:")
        print(robot.collect_data())

        print("\nTesting execute_command (start_video_stream):")
        print(robot.execute_command("start_video_stream"))

        print("\nTesting execute_command (unknown command):")
        print(robot.execute_command("unknown_command"))

    except ImportError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))


# Run the test
if __name__ == "__main__":
    test_yan_robot()
