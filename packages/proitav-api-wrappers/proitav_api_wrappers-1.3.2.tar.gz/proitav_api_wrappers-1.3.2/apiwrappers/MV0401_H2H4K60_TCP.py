from apiwrappers.MV0401_H2H4K60 import MV0401_Device
import socket
import logging
import time

# Configure logging
logging.basicConfig(filename="rs232.log", level=logging.INFO)


class MV0401_Device_TCP(MV0401_Device):
    def __init__(self, ip_address="10.0.50.22", port=4999, device_name=None) -> None:
        super().__init__(device_name)
        self.control = "TCP"
        self.ip_address = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip_address, self.port))

    def send_command(self, command) -> str:
        command_encoded = command.encode("ascii") + b"\r\n"
        logging.info(f"Sent: {command}")  # Log sent command
        print(f"Sent: {command}")
        self.sock.sendall(command_encoded)
        data = self.sock.recv(1024)
        time.sleep(0.25)

        if not data:
            logging.info("No response received")  # Log lack of response
            print("No response received")
            return "No response received"
        else:
            data_decoded = data.decode("ascii").strip()
            logging.info(f"Received: {data_decoded}")  # Log received data
            print(f"Received: {data_decoded}")
            return data_decoded


if __name__ == "__main__":
    device = MV0401_Device_TCP()
    device.get_firmware_ver()
    device.get_input_video_info(1)
    device.get_input_video_info(2)
    device.get_input_video_info(3)
    device.get_input_video_info(4)
