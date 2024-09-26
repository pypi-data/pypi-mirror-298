import platform
import psutil
from abc import ABC, abstractmethod


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

    @abstractmethod
    def setup_telemetry(self, config):
        pass


class DesktopAgent(DeviceInterface):
    def __init__(self):
        self.system_info = platform.uname()

    def get_device_info(self):
        return {
            "name": "Desktop Agent",
            "type": "desktop",
            "system": self.system_info.system,
            "release": self.system_info.release,
        }

    def collect_data(self):
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "cpu_usage": cpu_percent,
            "memory_total": memory.total,
            "memory_available": memory.available,
            "memory_percent": memory.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_free": disk.free,
            "disk_percent": disk.percent,
        }

    def execute_command(self, command_name, **kwargs):
        if command_name == "get_process_list":
            return self._get_process_list()
        else:
            return {
                "success": False,
                "message": "Unknown command: {}".format(command_name),
            }

    def setup_telemetry(self, config):
        # Implement telemetry setup logic here
        # This could involve setting up logging, metrics, or other monitoring tools
        print(f"Setting up telemetry for Desktop Agent with config: {config}")
        # For now, we'll just print the config. In a real implementation,
        # you might set up logging, configure metrics exporters, etc.

    def _get_process_list(self):
        try:
            processes = []
            for proc in psutil.process_iter(["pid", "name", "status"]):
                processes.append(proc.info)
            return {
                "success": True,
                "message": "Process list retrieved successfully",
                "data": processes,
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to retrieve process list: {}".format(str(e)),
                "error": str(e),
            }


# Test function
def test_desktop_agent():
    try:
        agent = DesktopAgent()
        print("DesktopAgent initialized successfully.")

        print("\nTesting setup_telemetry:")
        agent.setup_telemetry({"log_level": "INFO", "metrics_interval": 60})

        print("\nTesting get_device_info:")
        print(agent.get_device_info())

        print("\nTesting collect_data:")
        print(agent.collect_data())

        print("\nTesting execute_command (get_process_list):")
        result = agent.execute_command("get_process_list")
        print("Success:", result["success"])
        print("Message:", result["message"])
        print(
            "Number of processes:", len(result["data"]) if result["success"] else "N/A"
        )

        print("\nTesting execute_command (unknown command):")
        print(agent.execute_command("unknown_command"))

    except ImportError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))


# Run the test
if __name__ == "__main__":
    test_desktop_agent()
