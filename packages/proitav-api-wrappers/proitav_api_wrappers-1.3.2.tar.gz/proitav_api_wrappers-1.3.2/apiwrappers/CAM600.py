import telnetlib
import socket
import time
import logging


logger = logging.getLogger(__name__)


class CAM600_Device:
    def __init__(self, host, timeout=5, debug=False, max_retries=3):
        self.host = host
        self.timeout = timeout
        self.debug = debug
        self.tn = None
        self.max_retries = max_retries
        self.connection_attempted = False  # New flag to track connection attempts

    def _connect(self):
        if self.connection_attempted:
            return  # Skip connection attempts if already tried

        retries = 0
        self.connection_attempted = True  # Mark connection as attempted

        while retries < self.max_retries:
            try:
                self.tn = telnetlib.Telnet(self.host, port=23, timeout=self.timeout)
                if self.debug:
                    self.tn.set_debuglevel(2)
                self.tn.read_until(b"username:", timeout=self.timeout)
                time.sleep(0.1)
                self.tn.write(b"admin\n")
                self.tn.read_until(b"password:", timeout=self.timeout)
                time.sleep(0.1)
                self.tn.write(b"\n")
                self.tn.read_until(b"\r\n~ # ", timeout=self.timeout)
                print("Connected to CAM600")
                return  # Successfully connected
            except TimeoutError:
                print(
                    f"Connection to {self.host} timed out. Attempt {retries + 1} of {self.max_retries}"
                )
            except socket.error as e:
                print(f"Socket error: {e}. Attempt {retries + 1} of {self.max_retries}")
            except Exception as e:
                print(
                    f"Error connecting to {self.host}: {e}. Attempt {retries + 1} of {self.max_retries}"
                )

            retries += 1
            time.sleep(1)  # Optionally wait before retrying

        print(f"Failed to connect to {self.host} after {self.max_retries} attempts.")
        self.tn = None  # Ensure tn is set to None if all attempts fail

    def send(self, command):
        if (
            not self.tn and not self.connection_attempted
        ):  # Only try to connect if not already attempted
            self._connect()

        if self.tn:
            try:
                self.tn.write(command.encode("ascii") + b"\n")
                self.tn.read_until(b"\r\n", timeout=self.timeout)
                response = (
                    self.tn.read_until(b"~", timeout=self.timeout)
                    .decode("ascii")
                    .strip("~")
                    .strip()
                )
                self.tn.read_until(b"~ # \r\n~ ", timeout=0.25)
                return response
            except Exception as e:
                print(f"Error sending command: {e}")
                return None
        else:
            print("Connection not established, cannot send command.")
            return None

    def test_connection(self, debug=False) -> str:
        self.debug = debug
        connection_start = time.time()
        self._connect()
        connection_time = round(time.time() - connection_start, 2)

        responses = []
        message = "gbconfig -s device-info"
        tries = 20
        messages_start = time.time()
        for i in range(tries):
            responses.append(self.send(message))
        messages_time = round(time.time() - messages_start, 2)

        total_time = round(connection_time + messages_time, 2)

        from collections import Counter

        response_counts = Counter(responses)
        most_common_response = response_counts.most_common(1)[0]
        correct_responses = most_common_response[1]

        if self.tn:
            self.tn.close()
            string = f'Message: "{message}" | Attempts: {tries}\nSample Response: {responses[0]}\nConnection Time: {connection_time}\nMessages Time: {messages_time}\nTotal Time: {total_time}\nCorrect Responses: {correct_responses}'
            return string
        else:
            return f"Failed to connect to {self.host}"

    def get_device_info(self) -> dict:
        """
        Get device information.

        Returns:
            dict: A dictionary containing 'model', 'firmware', and 'build_date'.
        """
        response = self.send("gbconfig --device-info")
        response_lines = response.splitlines()

        if len(response_lines) < 3:
            logger.error("Unexpected response format")
            return {"error": "Unexpected response format"}

        return {
            "model": response_lines[0],
            "firmware": response_lines[1],
            "build_date": response_lines[2],
        }

    def set_ptz_direction(self, direction: str) -> int:
        """
        Set PTZ direction.

        Args:
            direction (str): Direction ('r' for right, 'l' for left, 'u' for up, 'd' for down).

        Returns:
            int: Response code from the device.

        Raises:
            ValueError: If the response cannot be converted to an integer.
        """
        valid_directions = {"r": "l", "l": "r", "u": "u", "d": "d"}
        if direction not in valid_directions:
            raise ValueError("Invalid direction. Use 'r', 'l', 'u', or 'd'.")

        response = self.send(
            f"gbconfig --camera-autocoord {valid_directions[direction]}"
        )
        try:
            return int(response.strip())
        except ValueError:
            logger.error(f"Unexpected response format for camera-autocoord: {response}")
            raise

    def set_ptz_reset(self):
        """Reset camera current position and zoom"""
        self.send("gbconfig --reset-camera-ptz")

    def set_tracking_mode(self, prm):
        """Set camera tracking mode
        prm = {0: off, 1: autoframing, 2: speaker tracking, 3: presenter tracking}
        """
        self.send(f"gbconfig --camera-mode {prm}")

    def set_zoom(self, zoom_level: float) -> str:
        """
        Set camera zoom level.

        Args:
            zoom_level (float): Zoom level between 1.0 and 6.0.

        Returns:
            str: Response from the device.

        Raises:
            ValueError: If the zoom level is outside the range.
        """
        if not (1.0 <= zoom_level <= 6.0):
            raise ValueError("Zoom level must be between 1.0 and 6.0")

        zoom_value = int(zoom_level * 100)  # Convert zoom to device-specific value
        return self.send(f"gbconfig --camera-zoom {zoom_value}")

    def get_zoom(self) -> int:
        """
        Get the current camera zoom level.

        Returns:
            int: Current zoom level as an integer.
        """
        response = self.send("gbconfig -s camera-phymaxzoom")
        try:
            return int(response.strip())
        except ValueError:
            logger.error(
                f"Unexpected response format for camera-phymaxzoom: {response}"
            )
            raise

    def preset_save(self, preset):
        """Save the current ptz to a preset
        preset = {1-9}"""
        response = self.send(f"gbconfig --camera-savecoord {preset}")
        return response

    def preset_call(self, preset):
        """Recall a preset
        preset = {1-9}"""
        response = self.send(f"gbconfig --camera-loadcoord {preset}")
        return response

    def set_mirror_invert(self, mirror, invert):
        """Set Mirror and Invert settings
        mirror = {0:no | 1:yes}
        invert = {0:no | 1:yes}
        """
        response = self.send(f"gbconfig --camera-mirror {mirror} {invert}")
        return response

    def set_powerline_freq(self, freq: int) -> bool:
        """Set Powerline Frequency
        freq = {50:50hz | 60:60hz}"""
        response = self.send(f"gbconfig --camera-powerfreq {freq}")
        if response == "1":
            return True
        else:
            return False

    def set_hd_mode(self, mode: int) -> bool:
        """Set HD Mode. Will cause camera to reboot
        mode = {0:no | 1:yes}"""
        response = self.send(f"gbconfig --camera-hd {mode}")
        if response == "1":
            return True
        else:
            return False

    def set_off_tracking_mode(self, effect, pip, pos):
        """
        effect = { 0:immediate | 1:smooth }
        pip = { 0:n | 1:y }
        pos = { 0:lu | 1:rd }
        """
        # BUG: This command does not work.
        response = self.send(f"gbconfig --camera-offtracking {effect} {pip} {pos}")
        return response

    def set_auto_tracking_mode(self, effect):
        """
        effect = { 0:immediate | 1:smooth }
        """
        # BUG: This command does not work.
        response = self.send(f"gbconfig --camera-autoframing {effect} 0 0")
        return response

    def set_auto_framing_speed(self, speed: int) -> bool:
        """Set Auto Framing Speed
        speed = { 0:slow | 1:normal | 2:fast }"""
        # BUG: I see no difference in speed when I change this.
        response = self.send(f"gbconfig  --camera-autoframingspeed {speed}")
        if response == "1":
            return True
        else:
            return False

    def get_auto_framing_speed(self) -> int:
        """
        Get the current auto framing speed setting.

        Returns:
            int: The auto framing speed value
                0: Slow
                1: Normal
                2: Fast

        Raises:
            ValueError: If the response cannot be converted to an integer
        """
        response = self.send("gbconfig -s camera-autoframingspeed")
        try:
            return int(response.strip())
        except ValueError:
            logger.error(
                f"Unexpected response format for auto framing speed: {response}"
            )
            raise

    def set_speaker_tracking_mode(self, effect: int, pip: int, pos: int, disp: int):
        """
        Set camera speaker tracking mode configuration.

        Parameters:
        effect (int): 0 for immediate, 1 for smooth
        pip (int): 0 for no picture-in-picture, 1 for yes
        pos (int): 0 for left upper, 1 for right down
        disp (int): 0 for normal display, 1 for gallery display

        Returns:
        str: Response from the camera
        """
        # BUG: What is Gallery?
        if (
            effect not in (0, 1)
            or pip not in (0, 1)
            or pos not in (0, 1)
            or disp not in (0, 1)
        ):
            raise ValueError(
                "Invalid parameter values. All parameters must be either 0 or 1."
            )

        response = self.send(
            f"gbconfig --camera-speakertracking {effect} {pip} {pos} {disp}"
        )
        return response

    def get_speaker_tracking_mode(self) -> dict:
        """
        Get the current speaker tracking mode of the camera.

        Returns:
            dict: The speaker tracking mode
        """
        response = self.send("gbconfig -s camera-speakertracking")
        values = response.strip().split()

        if len(values) != 4:
            logger.error(f"Unexpected response format: {response}")
            return {"error": "Unexpected response format"}

        try:
            return {
                "effect": int(values[0]),  # 0: immediate, 1: smooth
                "pip": bool(int(values[1])),  # 0: off, 1: on
                "pos": int(values[2]),  # 0: left upper, 1: right down
                "display": int(values[3]),  # 0: normal, 1: gallery
            }
        except ValueError as e:
            logger.error(f"Error parsing response: {e}")
            return {"error": f"Error parsing response: {e}"}

    def set_speaker_tracking_speed(self, speed: int) -> bool:
        """
        Set camera speaker tracking speed.

        Parameters:
        speed (int): 0 for slow, 1 for normal, 2 for fast

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if speed not in (0, 1, 2):
            raise ValueError("Invalid speed value. Must be 0, 1, or 2.")

        response = self.send(f"gbconfig --camera-speakertrackingspeed {speed}")
        if response == "1":
            return True
        else:
            return False

    def get_speaker_tracking_speed(self) -> int:
        """
        Get the current speaker tracking speed of the camera.

        Returns:
            int: The speaker tracking speed value
                0: Slow
                1: Normal
                2: Fast
        """
        response = self.send("gbconfig -s camera-speakertrackingspeed")
        try:
            return int(response.strip())
        except ValueError:
            logger.error(
                f"Unexpected response format for speaker tracking speed: {response}"
            )
            raise

    def set_presenter_tracking_mode(self, pip: int, pos: int):
        """
        Set camera presenter tracking mode configuration.

        Parameters:
        pip (int): 0 for no picture-in-picture, 1 for yes
        pos (int): 0 for left upper, 1 for right lower
        """

        response = self.send(f"gbconfig --camera-presentertracking 0 {pip} {pos}")
        return response

    def get_presenter_tracking_mode(self) -> int:
        """
        Get the current presenter tracking mode of the camera.

        Returns:
            dict: The presenter tracking mode
        """
        response = self.send("gbconfig -s camera-presentertracking")
        values = response.strip().split()

        if len(values) != 3:
            logger.error(f"Unexpected response format: {response}")
            return {"error": "Unexpected response format"}

        try:
            return {
                "effect": int(values[0]),  # 0: immediate, 1: smooth
                "pip": bool(int(values[1])),  # 0: off, 1: on
                "pos": int(values[2]),  # 0: left upper, 1: right lower
            }
        except ValueError as e:
            logger.error(f"Error parsing response: {e}")
            return {"error": f"Error parsing response: {e}"}

    def set_device_name(self, name: str) -> str:
        """
        Set the device name.

        Args:
            name (str): The new name for the device (1-20 characters, only letters, numbers, '_' or '-' allowed).

        Returns:
            str: Response from the device.

        Raises:
            ValueError: If the name contains invalid characters.
        """
        if not (1 <= len(name) <= 20) or not all(
            c.isalnum() or c in ("_", "-") for c in name
        ):
            raise ValueError(
                "Device name must be 1-20 characters, using letters, numbers, '_' or '-'."
            )

        return self.send(f"gbconfig --device-name {name}")

    def set_room_name(self, room: str):
        """
        Set the device room.
        Parameters:
        room (str): The new room for the device 1-20 characters (letters, numbers, '_' or '-' only)
        """
        if not all(c.isalnum() or c in ("_", "-") for c in room):
            raise ValueError(
                "Invalid characters in device room. Only letters, numbers, '_' and '-' are allowed."
            )

        response = self.send(f"gbconfig --room-name {room}")
        return response

    def set_network_dhcp(self) -> bool:
        """
        Set the network to DHCP
        """
        response = self.send("gbconfig --lan-info 0")
        if response == "1":
            return True
        else:
            return False

    def set_network_static(self, ipaddr, subnet, gateway):
        """
        Set the network to static. Unit will reboot.
        ipaddr = {xx.xx.xx.xx | ip address}
        subnet = {xx.xx.xx.xx | subnet mask}
        gateway = {xx.xx.xx.xx | gateway ip address}
        """

        def is_valid_ip(ip):
            parts = ip.split(".")
            return len(parts) == 4 and all(
                part.isdigit() and 0 <= int(part) <= 255 for part in parts
            )

        if not all(is_valid_ip(ip) for ip in [ipaddr, subnet, gateway]):
            raise ValueError(
                "Invalid IP address format. Please use the format xx.xx.xx.xx"
            )

        response = self.send(f"gbconfig --lan-info 2 {ipaddr} {subnet} {gateway}")
        return response

    def set_network_conflict(self, mode) -> bool:
        """
        Set the network conflict mode.
        mode = {0: off | 1: on}
        """
        response = self.send(f"gbconfig --ip-conflict {mode}")
        if response == "1":
            return True
        else:
            return False

    def set_standby_indicator(self, mode) -> bool:
        """
        Set the standby indicator light mode.

        Args:
            mode (int): The mode for the standby indicator light.
                0: White breathing effect
                2: Solid red
                255: Off

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        response = self.send(f"gbconfig --standby-indicator {mode}")
        if response == "1":
            return True
        else:
            return False

    def reboot(self) -> str:
        """Reboot the device."""
        return self.send("gbcontrol --reboot")

    def factory_reset(self) -> str:
        """Factory reset the device."""
        return self.send("gbcontrol --reset-to-default")

    def get_tracking_off_info(self) -> dict:
        """
        Get the current tracking off info.

        Returns:
            dict: The tracking off info
        """
        response = self.send("gbconfig -s camera-offtracking")

        # Split the response into individual values
        values = response.strip().split()

        # Ensure we have exactly 3 values
        if len(values) != 3:
            logger.error(f"Unexpected response format: {response}")
            return {"error": "Unexpected response format"}

        # Parse the values and create a dictionary
        try:
            info = {
                "effect": bool(int(values[0])),  # 0: immediate, 1: smooth
                "pip": bool(int(values[1])),  # 0: off, 1: on
                "pip_position": bool(int(values[2])),  # 0: left upper, 1: right down
            }
            return info
        except ValueError as e:
            logger.error(f"Error parsing response: {e}")
            return {"error": f"Error parsing response: {e}"}

    def get_powerline_freq(self) -> int:
        """
        Get the current powerline frequency.

        Returns:
            int: The powerline frequency
        """
        response = self.send("gbconfig -s camera-powerfreq")

        return int(response)

    def get_camera_mode(self) -> dict:
        """
        Get the current camera mode.

        Returns:
            dict: The camera mode
        """
        response = self.send("gbconfig -s camera-mirror")
        values = response.strip().split()

        if len(values) != 2:
            logger.error(f"Unexpected response format: {response}")
            return {"error": "Unexpected response format"}

        try:
            return {"mirror": bool(int(values[0])), "inverted": bool(int(values[1]))}
        except ValueError as e:
            logger.error(f"Error parsing response: {e}")
            return {"error": f"Error parsing response: {e}"}

    def get_camera_hd(self) -> bool:
        response = self.send("gbconfig -s camera-hd")
        try:
            return bool(int(response.strip()))
        except ValueError:
            logger.error(f"Unexpected response format for camera-hd: {response}")
            return False

    def get_all_offtracking_info(self) -> dict:
        camera_mode = self.get_camera_mode()
        tracking_info = self.get_tracking_off_info()
        powerline_freq = self.get_powerline_freq()
        camera_hd = self.get_camera_hd()

        return {
            "camera_mode": camera_mode,
            "tracking_info": tracking_info,
            "powerline_freq": powerline_freq,
            "camera_hd": camera_hd,
        }

    def get_all_speaker_tracking_info(self) -> dict:
        speaker_tracking_mode = self.get_speaker_tracking_mode()
        speaker_tracking_speed = self.get_speaker_tracking_speed()
        return {
            "speaker_tracking_mode": speaker_tracking_mode,
            "speaker_tracking_speed": speaker_tracking_speed,
        }

    def get_tracking_mode(self) -> int:
        """
        Get the current tracking mode of the camera.

        Returns:
            int: The tracking mode value.
                0: Off
                1: Auto framing
                2: Speaker tracking
                3: Presenter tracking

        Raises:
            ValueError: If the response cannot be converted to an integer.
        """
        response = self.send("gbconfig -s camera-mode")
        try:
            return int(response.strip())
        except ValueError:
            logger.error(f"Unexpected response format for camera-mode: {response}")
            raise


if __name__ == "__main__":
    cam = CAM600_Device("10.0.110.205", debug=False)
    print(cam.test_connection())
