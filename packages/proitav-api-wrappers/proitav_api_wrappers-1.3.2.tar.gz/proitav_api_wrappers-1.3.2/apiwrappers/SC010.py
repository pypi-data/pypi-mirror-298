"""Python Wrapper for SC010 using Telnet"""

from telnetlib import Telnet
import json
import logging
from time import sleep

logger = logging.getLogger(__name__)


# Helpers
def string_to_dict(message: str) -> dict:
    # Splitting by lines and then by ':'
    try:
        data_lines = message.strip().split("\n")
        data_dict = {}
        for line in data_lines:
            key, value = line.split(": ")
            data_dict[key.strip()] = value.strip()

        return data_dict
    except Exception as e:
        print(f"Error converting string to dictionary: {e}")
        return {}


def strip_to_dict(message: str) -> dict:
    try:
        brace_position = message.find("{")

        # Slice the string from the brace to the end if '{' is found
        if brace_position != -1:
            stripped_string = message[brace_position:]
        else:
            stripped_string = message

        return json.loads(stripped_string)
    except Exception as e:
        print(f"Error converting string to dictionary: {e}")
        return {}


class SC010_Device:
    def __init__(self, ip) -> None:
        self.ip = ip
        self.port = 23
        self.tn = None
        self.connect()

    def connect(self):
        """
        Attempts to connect to the device, handling cases where the device might be offline or not responding.
        """
        if self.tn is None:
            self.tn = Telnet()  # Initialize without connecting
        try:
            self.tn.open(self.ip, self.port, timeout=1.0)
            self.tn.read_until(b"welcome to use hdip system.")
            # print("Connected")
            return True
        except Exception as e:
            print(f"Failed to connect to SC010 at {self.ip}. Error: {e}")
            self.tn = None  # Reset the connection
            return False

    def ensure_connection(func):
        """
        Decorator to ensure there's a connection before executing a command.
        """

        def wrapper(self, *args, **kwargs):
            if not self.tn:
                print("Reconnecting...")
                if not self.connect():
                    return None  # or handle as needed
            return func(self, *args, **kwargs)

        return wrapper

    def flush(self):
        """Flushes any pending responses from the buffer."""
        if self.tn:
            self.tn.read_very_eager()

    @ensure_connection
    def send(self, command):
        """
        Sends a command to the device, ensuring the device is connected.
        """
        try:
            self.flush()
            self.tn.write(command.encode("ascii") + b"\n")
            response = self.tn.read_until(b"\r\n\r\n")
            return response.decode()
        except Exception as e:
            print(f"Error sending command: {e}")
            self.tn = None  # Reset the connection in case of error
            return None

    def disconnect(self):
        """
        Safely closes the Telnet connection if it exists.
        """
        if self.tn is not None:
            try:
                self.tn.close()
                # print("Disconnected")
            except Exception as e:
                print(f"Error closing Telnet connection: {e}")
            finally:
                self.tn = None

    def _strip_prefix(self, response):
        """Strips everything before the first [ or { character."""
        start_bracket = response.find("[")
        start_brace = response.find("{")
        start = min(
            start_bracket if start_bracket != -1 else float("inf"),
            start_brace if start_brace != -1 else float("inf"),
        )
        if start != float("inf"):
            return response[start:]
        return response

    def get_version(self) -> dict:
        response = self.send("config get version")
        dict = string_to_dict(response)
        self.api_version = dict.get("API version")
        self.system_version = dict.get("System version")
        return dict

    def get_system_info(self) -> dict:
        response = self.send("config get system info")
        dict = strip_to_dict(response)
        return dict

    def __str__(self):
        return f"Controller@{self.ip} System Version:{self.version.get('System version')} API Version:{self.version.get('API version')}"

    # Config Commands
    def set_ip4addr(self, ipaddr=None, netmask=None, gateway=None):
        """
        Configures network settings in LAN(AV) port for communicating with devices
        Note:
        This command is used to set IP address, subnet mask and gateway in LAN(AV) port. You can set two or three of them at the same time or only one each time.
        LAN(AV) port only supports Static IP mode. After network settings are configured, it automatically reboots for the settings to take effect.
        """
        command = "config set "
        if ipaddr is not None:
            command += f"ip4addr {ipaddr}"
        if netmask is not None:
            command += f"netmask {netmask}"
        if gateway is not None:
            command += f"gateway {gateway}"

        return self.send(command)

    def set_ipaddr2(self, ipaddr=None, netmask=None, gateway=None):
        """Configures network settings in LAN(C) port for communicating with devices
        Note:
        This command is used to set IP address, subnet mask and gateway in LAN(AV) port. You can set two or three of them at the same time or only one each time.
        LAN(C) port only supports Static IP mode. After network settings are configured, it automatically reboots for the settings to take effect.
        """
        command = "config set "
        if ipaddr is not None:
            command += f"ip4addr {ipaddr}"
        if netmask is not None:
            command += f"netmask {netmask}"
        if gateway is not None:
            command += f"gateway {gateway}"

        return self.send(command)

    def set_webloginpasswd(self, password):
        """Sets WebUI login password"""
        command = f"config set webloginpasswd {password}"
        return self.send(command)

    def set_telnetpasswd(self, password):
        """Sets Telnet configuration page login password"""
        command = f"config set telnetpasswd {password}"
        return self.send(command)

    def set_telnetpasswd_delete(self):
        """Delete Telnet configuration page login password"""
        command = "config set delete telnetpasswd"
        return self.send(command)

    def set_device_alias(self, hostname, alias):
        """Set's an alias for device and alias can be used in other commands
        instead of hostname"""
        command = f"config set device alias {hostname} {alias}"
        return self.send(command)

    def set_device_remove(self, *hostnames):
        """Remove devices from Controller record. Can remove one or multiple
        devices at once.
        Args:
        Hostname1
        Hostname2
        ..."""
        command = "config set device remove "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def set_device_ip(self, hostname, type, ipaddr=None, netmask=None, gateway=None):
        """Set device network configuration
        Args:
        hostname = ex: IPD5100-341B22800BCD
        type = (autoip, dhcp, static)
                autoip = set the device to a self assigned 169.254.xxx.xxx address
                dhcp = get IP address from DHCP server
                static = need to also provide ipaddr, netmask, gateway
                    ex: IPD5100-341B22800BCD static 192.168.1.20 255.255.255.0 192.168.1.1
        """
        if type.lower() == "static":
            command = (
                f"config set device ip {hostname} {type} {ipaddr} {netmask} {gateway}"
            )
        else:
            command = f"config set device ip {hostname} {type}"
        return self.send(command)

    def set_device_info(self, command, *hostnames):
        """
        Changes a device's one or multiple working parameters in key=value format.
        You can change parameters for multiple devices at one time.

        ex: set_device_info(
            "IPD5100-341B22800BCD",
            "IPD5100-341B22800BCC",
            command="sinkpower.mode=4004"
        )

        Note:
        hostname1 and hostname2 are device names.
        command is a string in key=value format.
        """
        full_command = f"config set device info {command} {' '.join(hostnames)}"
        return self.send(full_command)

    def set_device_audio(self, type, *hostnames):
        """This command is only used for IPE5000,
        configure device hostname1, hostname2's audio input type such as auto, hdmi, analog.
        """
        command = f"config set device audio input type {type} "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def set_device_notify_status(self, on_off, *hostnames):
        """Wakes up device status notify or makes it enter its standby mode. hostname is the device alias;
        Hostname also can be KEY words: ALL_DEV, ALL_TX, ALL_RX, ALL_MRX, ALL_WP, ALL_GW, when hostname is one of the KEY word,
        this command will not include other KEY word and device name.
        Note:
        •	This command is available for IPX2000.
        •	When the system work mode is set as 1, this command will be not available.
        """
        command = f"config set device status notify {on_off} "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def set_device_notify_cec(self, on_off, *hostnames):
        """Wakes up device cec notify system or makes it enter its standby mode. hostname is the device alias;
        Hostname also can be KEY words: ALL_DEV, ALL_TX, ALL_RX,
        when hostname is one of the KEY word, this command will not include other KEY word and device name.
        """
        command = f"config set device cec notify {on_off} "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def set_device_audio_volume(self, action, type, *hostnames):
        """Control device audio volume, the meanings of parameters as follow:
        {mute|unmute|up|down}: up is volume increased; down is volume decreased; mute means mute mode, unmute means mute mode cancelled;
        {hdmi[:n]|analog[:n]|all}: hdmi means that all the HDMI audio outputs, hdmi[:n] means that the number of hdmi audio output is n; analog means that all the analog audio outputs, analog[:n]means that the number of analog audio output is n; all is all of the hdmi and analog audio outputs.
        Note: IPX5000 supports "up" and "down" setting for analog audio only.
        """
        command = f"config set device audio volume {action} {type} "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def set_device_video_source(self, type, hostname):
        """Configure input video signal type for TX; the signal type supports three modes: auto, hdmi and dp.
        Note: This command is available for IPX6000 only.
        """
        command = f"config set device videosource {hostname} {type}"
        return self.send(command)

    def set_device_audio_source(self, type, hostname):
        """Configure HDMI audio source type for RX; the source type supports three modes: hdmi (digital audio, corresponds to audio from DP input or HDMI input), analog and dmix.
        Note: This command is available for IPX6000 only.
        """
        command = f"config set device audiosource {hostname} {type}"
        return self.send(command)

    def set_device_audio_source2(self, type, hostname):
        """Configure audio source type for RX's analog output port; the source type supports two modes: analog and dmix.
        Note: This command is available for IPX6000 only.
        """
        command = f"config set device audio2source {hostname} {type}"
        return self.send(command)

    def set_device_mode(self, mode, hostname):
        """Set device mode
        mode: RECEIVER, TRANSMITTER or TRANSCEIVER"""
        command = (
            f"config set device info device_mode={mode.upper()} {hostname.upper()}"
        )
        return self.send(command)

    def set_session_alias(self, on_off):
        """Open or close the alias mode on the current session, if the value set to be on, then all API command next to it will get alias information feedback, while the feedback got alias. If the value set to be off, then all
        API command next to it will get true name information feedback."""
        command = f"config set session alias {on_off}"
        return self.send(command)

    def set_session_telnet_alias(self, on_off):
        """Configure the Telnet session default alias mode, it will not affect the telnet session that has been linked, only affect the telnet session which is linked later. When the value is on, the API response will describe the device with alias. When the value is off, the API response will describe the device with true name.
        Note: on is by default.
        """
        command = f"config set telnet alias {on_off}"
        return self.send(command)

    def set_session_rs232_alias(self, on_off):
        """Configure uart session alias mode. When it is on, the API response will describe the device with alias, when is off, API response will describe the device with true name.
        Note: on is by default.
        """
        command = f"config set rs-232 alias {on_off}"
        return self.send(command)

    def set_system_ssh(self, on_off):
        """Open or close the system SSH service, off is by default."""
        command = f"config set systemsshservice {on_off}"
        return self.send(command)

    def set_system_workmode(self, status):
        """Set the working mode for the system. By default, it is set as mode 1.
        0: In this mode, all the IP series units except IPX6000 are available for API control.
        1: In this mode, IPX6000 is available for API control, while the other IP series units will be unavailable for API “Notify devices status”.
        Note:
        Please reboot the unit for this command setting to take effect.
        status = 0 or 1
        """
        command = f"config set system workmode {status}"
        return self.send(command)

    def set_system_preview(self, fps):
        """Set the total preview framerate for the IP6000 series TX units in the system; the range is [0,30], and the type is integer.
        By default, the framerate is set as 0.
        •	0: The preview function is disabled.
        •	Other value: The preview function for IP6000 TX is enabled; the preview framerate for each TX is calculated by system (=total framerate/quantity of online TX), the minimum framerate is 0.5.
        """
        command = f"config set system preview fps {fps}"
        return self.send(command)

    def set_scene(self, scene):
        """Set scene"""
        return self.send(f"scene active {scene}")

    def get_devicelist(self) -> list:
        """Get all online device names"""
        command = "config get devicelist"
        response = self.send(command)
        cleaned_str = response.replace("devicelist is ", "").strip()
        device_list = cleaned_str.split(" ")
        return device_list

    def get_ipsettings(self, lan=1):
        """Get network settings for LAN(AV) or LAN(C) and return as a dictionary.
        Args:
            lan: 1 or 2
                1. LAN(AV)
                2. LAN(C)
        Returns:
            A dictionary with port, ip4addr, netmask, and gateway.
        """
        if lan == 1:
            command = "config get ipsetting"
            port = "LAN(AV)"
        else:
            command = "config get ipsetting2"
            port = "LAN(C)"

        response = self.send(command)

        # Remove the "config get ipsetting" or "config get ipsetting2" part from the response
        if lan == 1:
            response = response.replace("ipsetting is:", "").strip()
        else:
            response = response.replace("ipsetting2 is:", "").strip()

        # Split the response into parts and parse into a dictionary
        settings_dict = {"port": port}
        parts = response.split(" ")
        for i in range(0, len(parts), 2):
            key = parts[i]
            value = parts[i + 1]
            settings_dict[key] = value

        return settings_dict

    def get_device_name(self, device=None):
        """Obtains device name or its alias.
        Note:
        You can use a device name to obtain its alias or vice versa.
        alias is device alias. hostname is device name.
        If you use a device name to obtain its alias which is not set, response is "NULL".
        If config get name is used without parameters, response is all device names and their aliases.
        """
        if device is None:
            command = "config get name"
        else:
            command = f"config get name {device}"
        return self.send(command)

    def get_device_info(self, *hostnames) -> dict:
        """Obtains device working parameters in real time.
        Note:
        hostname1 and hostname2 are device names.
        You can get one or multiple devices' working parameters at one time.
        Alias name feature is added from the API v1.7 version
        It may take some time for IP controller to get device information.
        The developer must consider this factor when programming the caller’s code.
        Working parameters use Key:Value format. Key is a parameter name and value is its value. For more information, see 3.1 Device Info section.
        """
        command = "config get device info "
        for hostname in hostnames:
            command += hostname + " "
        response = self.send(command)
        logger.debug(f"Raw response for device info: {response}")
        response = self._strip_prefix(response)

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}, response: {response}")
            return {}

    def get_device_status(self, *hostnames) -> dict:
        """Obtains device status in real time.
        Note:
        hostname1 and hostname2 are device names.
        Device status information uses json format.
        Devices' status information is depend on device instead of IP controller, IP controller is only used for passing by.
        """
        command = "config get device status "
        for hostname in hostnames:
            command += hostname + " "

        response = self.send(command)
        logger.debug(f"Raw response for device status: {response}")

        response = self._strip_prefix(response)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}, response: {response}")
            return {}

    def get_device_json(self) -> list:
        """Obtains all device information and returns a list of dictionaries.
        Note:
        "aliasName" represents device alias name (If no alias name appears, it means that this device is not given an alias name).
        "deviceType" represents device type: TX represents transmitter, RX represents receiver, TRX represents transceiver.
        "group" represents a group. One RX unit can only be put in one group. "sequence" in "group" represents the position of this group, which starts with 1. If "sequence" is 0, it means that this group is not arranged in specific order. In this case, you can put this group in a position based on programming.
        "ip" represents device IP address such as 169.254.5.24.
        "online" represents device status, online or offline. "true" represents device is online. "false" represents device is offline.
        "sequence" in a device represents the position of this device in its group, which starts with 1. If "sequence" is 0, it means that this device is not arranged in specific order. In this case, you can put this device in a position based on programming.
        "trueName" represents device true name.
        """
        response = self.send("config get devicejsonstring")
        logger.debug(f"Raw response for device json: {response}")

        response = self._strip_prefix(response)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}, response: {response}")
            return []

    def get_scene_json(self) -> dict:
        """Obtains all scene information.
        Note:
        "group" represents a group. One scene can only be put in one group. "sequence" in" group" represents the position of this group, which starts with 1. If "sequence" is 0, it means that this group is not arranged in specific order. In this case, you can put this group in a position based on programming.
        "layoutseq" represents the position of this scene in video wall.
        "n" and "m" represent the number of rows and columns respectively in a scene.
        "name" represents scene name, such as s
        "rxArray" describes RX in a form of two-dimensional array in a scene.
        "sequence" in a scene represents the position of video wall which contains this scene , which starts with 1. If "sequence" is 0, it means that this video wall is not arranged in specific order. In this case, you can put it in a position based on programming.
        "txListArray" describesTX in a form of two-dimensional array in a scene.
        "vwConfigList" represents the configuration of combination screen in a scene. "name" represents combination screen name, which uses "scene name_ combination screen name" in IP controller (SC010)."pos_row" represents the start place of the first row."pos_col" represents the start place of the first column."row_count" represents the number of rows in combination screen."col_count"represents the number of columns in combination screen.
        """
        command = "config get scenejsonstring"
        response = self.send(command)
        logger.debug(f"Raw response for scene json: {response}")

        response = self._strip_prefix(response)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}, response: {response}")
            return {}

    def get_telnet_alias(self):
        """Get the rs-232 alias mode."""
        command = "config get rs-232 alias"
        return self.send(command)

    def get_system_ssh(self):
        """Get the system SSH service mode."""
        command = "config get system sshservice"
        return self.send(command)

    def remove_device(self, *hostnames):
        """Removes hostnames from controller"""
        command = "config set device remove "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def device_cec_standby(self, *hostnames):
        """Send CEC standy to each host devices"""
        command = "config set device cec standby "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def device_cec_onetouchplay(self, *hostnames):
        """Send CEC one touch play to host devices"""
        command = "config set device cec onetouchplay "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def device_sinkpower(self, on_off, *hostnames):
        """Set display to wake up or enter standby"""
        command = f"config set device sinkpower {on_off} "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def device_reboot(self, *hostnames):
        """Reboot device/s"""
        command = "config set device reboot "
        for hostname in hostnames:
            command += hostname + " "

        return self.send(command)

    def device_factory_restore(self, *hostnames):
        """Factory restore devices"""
        command = "config set device restorefactory "
        for hostname in hostnames:
            command += hostname + " "
        return self.send(command)

    def disconnect_all(self):
        return self.send("matrix set NULL ALL_RX")

    def system_factory_restore(self):
        """Resets Controller to factory settings
        IP address will change 169.254.1.1"""
        command = "config set restorefactory"
        return self.send(command)

    def system_reboot(self):
        """Reboot Controller"""
        command = "config set reboot"
        return self.send(command)

    # Matrix Commands
    def set_matrix(self, segments):
        """
        example: matrix_set("TX1 RX1 RX2","TX2 RX3 RX4")
        Controls the switching of RX to TX.
        Parameters are separated by commas such as segments TX1 RX1 RX2,TX2 RX3 RX4.
        Every segment starts with TX and is followed by some RX which are switched to this TX.
        If a segment starts with TX whose name is "NULL" the followed RX will not decode video. "NULL" is not case sensitive.
        For RX in video wall, this command is used to switch to another TX but will not clear video wall settings.
        If a RX in video wall displays a certain position of TX1's video, after this RX is switched to TX2,
        RX will still display the same position of TX2's video. Other RX in video wall functions in the same way.
        For RX supporting multi-view, this command is used to switch to another TX for full-screen displaying.
        """
        command = "matrix set"
        segments = segments.split(",")  # Split segments by comma
        for i, segment in enumerate(segments):
            command += " " + segment.strip()  # Add each segment to the command
            if (
                i < len(segments) - 1
            ):  # Add comma after each segment except the last one
                command += ","
        return self.send(command)

    def get_matrix(self):
        """Obtains TX played by RX in matrix."""
        command = "matrix get"
        return self.send(command)

    # CEC
    def cec(self, command, *hosts):
        """Send CEC Command to device"""
        command = f'cec "{command}" '
        for host in hosts:
            command += host + " "
        return self.send(command)

    def find_me(self, seconds, *hosts):
        """Blink LEDS for seconds on device"""
        command = f"config set device findme {seconds} "
        for host in hosts:
            command += host + " "
        return self.send(command)

    def set_vw_add(self, name, nrows, ncols, encoder):
        """Add video wall"""
        command = f"vw add {name} {nrows} {ncols} {encoder}"
        return self.send(command)

    def get_vw(self):
        """Get video wall"""
        return self.send("vw get")

    def set_vw_change_source(self, vw_name, tx_name):
        """Change source of video wall"""
        command = f"vw change {vw_name} {tx_name}"
        return self.send(command)

    def set_vw_bezelgap(self, vw_name, ow, oh, vw, vh):
        """Set video wall bezel gap"""
        return self.send(f"vw bezelgap {vw_name} {ow} {oh} {vw} {vh}")

    def set_vw_stretch(self, vw_name, type):
        """Set video wall stretch

        type: fit, stretch, fill

        fit: The picture will scale in proportion; it will be displayed proportionally in maximized state; there may be blank space.
        stretch: The picture will scale out of proportion; it will be stretched and shown according to the screen resolution; there's no blank space.
        fill: The picture will scale in proportion to fill the screen; there's no blank space, while part of the picture may not be displayed.
        """
        return self.send(f"vw stretch {vw_name} {type}")

    def set_vw_remove(self, vw_name):
        """Remove video wall"""
        return self.send(f"vw rm {vw_name}")

    def set_vw_add_layout(self, vw_name, nrows, ncols, tx_hostname, *rx_hostnames):
        """Add layout to video wall"""
        command = f"vw add {vw_name} layout {nrows} {ncols} {tx_hostname}"
        for rx_hostname in rx_hostnames:
            command += f" {rx_hostname}"
        return self.send(command)

    def set_vw_change(self, rx_hostname, tx_hostname):
        """Remove RX from video and have it switch to TX in full picture"""
        return self.send(f"vw change {rx_hostname} {tx_hostname}")

    def help(self):
        """Prints out all functions available"""
        functions = [
            func
            for func in dir(self)
            if callable(getattr(self, func))
            and not func.startswith("__")
            and not func.startswith("_")
        ]
        num_functions = len(functions)
        print("Available functions:")
        for i in range(0, num_functions, 2):
            func_name_1 = functions[i]
            func_name_2 = functions[i + 1] if i + 1 < num_functions else ""
            print("{:<30}{:<30}".format(func_name_1, func_name_2))
        print("")

    def remove_offline_devices(self):
        """
        Removes all offline devices by calling controller.remove_device with their trueNames.

        :param controller: The controller instance that has get_device_json and remove_device methods.
        """
        # Get the device JSON from the controller
        device_json = self.get_device_json()

        # Filter for offline devices and extract their trueNames
        offline_device_names = [
            device["trueName"] for device in device_json if not device["online"]
        ]

        if offline_device_names:
            # Convert the list of names to a string if required by your controller.remove_device method
            # Assuming remove_device takes a list of hostnames; adjust if it takes a different format
            self.remove_device(*offline_device_names)
            print(f"Removed offline devices: {', '.join(offline_device_names)}")
        else:
            print("No offline devices found to remove.")


if __name__ == "__main__":
    controller = SC010_Device("192.168.50.165")
    decoders_6000 = "TV1-6000 TV2-6000 TV3-6000 TV4-6000"
    decoders_5100 = "TV1 TV2 TV3 TV4"
    controller.cec("ff82", decoders_5100)  # Power On
    sleep(20)
    controller.cec("ff440b", decoders_5100)  # Exit
    sleep(1)
    controller.cec("ff440d", decoders_5100)  # Back
    sleep(1)
    controller.cec("ff4403", decoders_5100)  # Left
    sleep(5)
    controller.cec("ff36", decoders_5100)  # Power Off

    # devices = controller.get_devicelist()
    # print(controller.get_device_status("BrightSign1"))
    # print(controller.get_device_status("BR5-6000"))
    # print(controller.set_scene("5100-wall"))

    # print(controller.get_device_status(devices[0]))
    # print(controller.get_device_info("BR5-6000"))

    # commands = [
    #     controller.get_version(),
    #     controller.get_system_info(),
    #     controller.get_device_info(),
    #     controller.get_device_json(),
    #     controller.get_devicelist(),
    #     controller.get_ipsettings(),
    # ]
    # for command in commands:
    #     print(command)
    #     print("\n")
