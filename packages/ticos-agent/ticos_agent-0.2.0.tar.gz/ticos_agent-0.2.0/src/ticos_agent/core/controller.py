from ..base import BaseDevice


class Controller:
    def __init__(self, device: BaseDevice):
        self.device = device

    def execute_command(self, command_name, **kwargs):
        return self.device.execute_command(command_name, **kwargs)
