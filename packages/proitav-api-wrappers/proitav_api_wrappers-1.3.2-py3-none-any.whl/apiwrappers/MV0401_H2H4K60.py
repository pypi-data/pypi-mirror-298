"""
Python Wrapper for MV0401-H2H4K60-000
Multiview 4k60
Key Features:
1.TRUE 4K@60HZ/UHD VIDEO: Both HDMI input and HDMI output compliant HDMI 2.0b specification up to 4K@60Hz 4:4:4 8bit.
2.RICH LAYOUT MODE: Support six screen layouts, such as Original, Dual-view, Master mode, H mode, PIP mode and Quad mode.
3.SEAMLESS SWITCHING: Supports seamless switching under the same layout.
4.CASCADE FUNCTION: More inputs are displayed on the same display.
5.IMAGE STRETCHING: Optional support fixed aspect ratio and image stretching mode.
6.AUDIO DE-EMBEDDING: Supports audio de-embedding from the HDMI output.
7.MULTIPLE CONTROL: Supports multiple control methods, including button, IR and RS232 control.


"""

import serial


class MV0401_Device_Serial:
    def __init__(self, device_name=None) -> None:
        """Python Wrapper for MV0401-H2H4K60-000
        Multiview 4k60
        Key Features:
        1.TRUE 4K@60HZ/UHD VIDEO: Both HDMI input and HDMI output compliant HDMI 2.0b specification up to 4K@60Hz 4:4:4 8bit.
        2.RICH LAYOUT MODE: Support six screen layouts, such as Original, Dual-view, Master mode, H mode, PIP mode and Quad mode.
        3.SEAMLESS SWITCHING: Supports seamless switching under the same layout.
        4.CASCADE FUNCTION: More inputs are displayed on the same display.
        5.IMAGE STRETCHING: Optional support fixed aspect ratio and image stretching mode.
        6.AUDIO DE-EMBEDDING: Supports audio de-embedding from the HDMI output.
        7.MULTIPLE CONTROL: Supports multiple control methods, including button, IR and RS232 control.

        Need to send RS232 device.
        Example: "/dev/ttyUSB0"
        Example: "COM3"
        """
        if device_name:
            self.init_serial(device_name)

    def init_serial(self, device_name):
        self.control = "RS232"
        self.device = device_name  # string
        self.rs232_baud = 115200
        self.rs232_data_bits = 8
        self.rs232_parity = "N"
        self.rs232_stop_bits = 1
        self.rs232_flow_control = "N"
        self.rs232_timeout = 1
        self.serial = serial.Serial(
            port=self.device,
            baudrate=self.rs232_baud,
            timeout=self.rs232_timeout,
            bytesize=self.rs232_data_bits,
            parity=self.rs232_parity,
            stopbits=self.rs232_stop_bits,
        )

    def send_command(self, command) -> str:
        """Send command, returns response"""
        command_encoded = command.encode("ascii") + b"\r\n"
        print(f"Sent: {command}")
        self.serial.write(command_encoded)
        data = self.serial.read_until(b"\r\n")

        if not data:
            print(f"No response received within {self.rs232_timeout}s")
            return f"No response received within {self.rs232_timeout}s"
        else:
            data_decoded = data.decode("ascii")
            print(f"Received: {data_decoded}")
            return data_decoded

    def get_firmware_ver(self):
        """Returns Firmware Version"""
        command = "GET VER"
        response = self.send_command(command)
        return response

    def set_video_mute(self, prm: int, prm1: int):
        """Turns On or Off video mute on source,
        prm = {0,1,2,3,4}
        1:hdmi in1 channel mute/unmute
        2:hdmi in2 channel mute/unmute
        3:hdmi in3 channel mute/unmute
        4:hdmi in4 channel mute/unmute
        0: hdmi output mute/unmute
        ※ prm1 = {0,1}// 1 means mute;0 means unmute"""
        command = f"SET VIDOUT_MUTE {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_video_mute_status(self, prm):
        """Returns Video Mute Status
        Returns: VIDOUT_MUTE x y
        prm = {0,1,2,3,4}
        1:hdmi in1 channel mute/unmute
        2:hdmi in2 channel mute/unmute
        3:hdmi in3 channel mute/unmute
        4:hdmi in4 channel mute/unmute
        0:hdmi output mute/unmute
        ※ prm1 = {0,1}// 1 means mute;0 means unmute"""
        command = f"GET VIDOUT_MUTE {prm}"
        response = self.send_command(command)
        return response

    def set_video_out_resolution(self, prm):
        """Set video output resolution mode
        prm = {0,1,2,3}
        0:Follow Sink prefer timing
        1:Force 4K@60
        2:Force 4K@30
        3:Force 1080p@60"""
        command = f"SET OUTPUT_RES {prm}"
        response = self.send_command(command)
        return response

    def get_video_out_resolution(self):
        """Returns video output resolution
        Parameter:
        prm = {0,1,2,3}
        0:Follow Sink prefer timing
        2:Force 4K@30
        1:Force 4K@60
        3:Force 1080p@60"""
        command = "GET OUTPUT_RES"
        response = self.send_command(command)
        return response

    def get_video_layout(self):
        """Returns Layout
        prm = {0,1,2,3,4,5}
        0:Original
        1:Dual-view
        2:Pip
        3:H
        4:Master
        5:Quad"""
        command = "GET OUTPUT_MODE"
        response = self.send_command(command)
        return response

    def set_video_layout(self, prm):
        """Set video output display layout
        prm = {0,1,2,3,4,5}
        0:Original
        1:Dual-view
        2:Pip
        3:H
        4:Master
        5:Quad"""
        command = f"SET OUTPUT_MODE {prm}"
        response = self.send_command(command)
        return response

    def set_audio_source(self, prm):
        """Set video original display layout source
        prm = {1,2,3,4}
        1:display hdmi in 1
        2:display hdmi in 2
        3:display hdmi in 3
        4:display hdmi in 4"""
        command = f"SET AUDOUT_SRC {prm}"
        response = self.send_command(command)
        return response

    def get_audio_source(self):
        """Returns Audio Source
        prm = {1,2,3,4}
        1:display hdmi in 1
        2:display hdmi in 2
        3:display hdmi in 3
        4:display hdmi in 4"""
        command = "GET AUDOUT_SRC"
        response = self.send_command(command)
        return response

    def set_layout_source_dual(self, prm: int, prm1: int):
        """Set video source for the dual display layout
        prm = {1,2,3,4}//left channel
        prm1 = {1,2,3,4}//right channel"""
        command = f"SET DUAL_SRC {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_layout_source_dual(self):
        """Returns video source for the dual display layout
        prm = {1,2,3,4}//left channel
        prm1 = {1,2,3,4}//right channel"""
        command = "GET DUAL_SRC"
        response = self.send_command(command)
        return response

    def set_layout_source_H(self, prm, prm1, prm2, prm3):
        """Set video source for the H display layout
        prm = {1,2,3,4}//left channel
        prm1 ={1,2,3,4}//top of the middle channel
        prm2 = {1,2,3,4}//bottom of the middle channel
        prm3 ={1,2,3,4}//right channel"""
        command = f"SET H_SRC {prm} {prm1} {prm2} {prm3}"
        response = self.send_command(command)
        return response

    def get_layout_source_H(self):
        """Returns video source for the H display layout
        prm = {1,2,3,4}//left channel
        prm1 ={1,2,3,4}//top of the middle channel
        prm2 = {1,2,3,4}//bottom of the middle channel
        prm3 ={1,2,3,4}//right channel"""
        command = "GET H_SRC"
        response = self.send_command(command)
        return response

    def set_layout_pip_source(self, prm, prm1):
        """Set video PIP mode  display layout source
        prm = {1,2,3,4}//big channel
        prm 1= {1,2,3,4}//small channel"""
        command = f"SET PIP_SRC {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_layout_pip_source(self):
        """Returns PIP video source
        prm = {1,2,3,4}//big channel
        prm 1 = {1,2,3,4}//small channel"""
        command = "GET PIP_SRC"
        response = self.send_command(command)
        return response

    def set_layout_quad_source(self, prm, prm1, prm2, prm3):
        """Set video QUAD display layout sources
        prm = {1,2,3,4}//top of the left channel
        prm1 = {1,2,3,4}//top of the right channel
        prm2 = {1,2,3,4}//bottom of the left channel
        prm3 = {1,2,3,4}//bottom of the right channel"""
        command = f"SET QUAD_SRC {prm} {prm1} {prm2} {prm3}"
        response = self.send_command(command)
        return response

    def get_layout_quad_source(self):
        """Returns the layout QUAD sources
        prm = {1,2,3,4}//top of the left channel
        prm1 = {1,2,3,4}//top of the right channel
        prm2 = {1,2,3,4}//bottom of the left channel
        prm3 = {1,2,3,4}//bottom of the right channel"""
        command = "GET QUAD_SRC"
        response = self.send_command(command)
        return response

    def set_layout_master_source(self, prm, prm1, prm2, prm3):
        """Sets video MASTER layout sources
        prm = {1,2,3,4}//top of the left channel
        prm1 = {1,2,3,4}//top of the right channel
        prm2 = {1,2,3,4}//bottom of the left channel
        prm3 = {1,2,3,4}//bottom of the right channel
        """
        command = f"SET MASTER_SRC {prm} {prm1} {prm2} {prm3}"
        response = self.send_command(command)
        return response

    def get_layout_master_source(self):
        """Returns video MASTER layout sources
        prm = {1,2,3,4}//top of the left channel
        prm1 = {1,2,3,4}//top of the right channel
        prm2 = {1,2,3,4}//bottom of the left channel
        prm3 = {1,2,3,4}//bottom of the right channel
        """
        command = "GET MASTER_SRC"
        response = self.send_command(command)
        return response

    def set_audio_mute(self, prm, prm1):
        """Set audio mute
        prm = {0,1}//0: hdmi out 1: av out
        prm1 = {0,1}//0: unmute 1: mute"""
        command = f"SET MUTE {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_audio_mute(self, prm):
        """Get audio mute status
        prm = {0,1}//0: hdmi out 1: av out
        prm1 = {0,1}//0: unmute 1: mute"""
        command = f"GET MUTE {prm}"
        response = self.send_command(command)
        return response

    def set_input_stretch(self, prm, prm1):
        """Set video input stretch
        prm = {1,2,3,4}
        1: hdmi in1
        2: hdmi in2
        3: hdmi in3
        4: hdmi in4
        prm1 = {0,1} // 0: stretch  1: full"""
        command = f"SET VIDIN_STRETCH {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_input_stretch(self, prm):
        """Set video input stretch
        prm = {1,2,3,4}
        1: hdmi in1
        2: hdmi in2
        3: hdmi in3
        4: hdmi in4
        prm1 = {0,1} // 0: stretch  1: full"""
        command = f"GET VIDIN_STRETCH {prm}"
        response = self.send_command(command)
        return response

    def get_hdcp_mode(self):
        """GET HDCP mode
        prm = {0,1,2,3,4}
        0: follow source
        1: follow sink
        2: hdcp disabled
        3: hdcp 1.4
        4: hdcp 2.2"""
        command = "GET HDCP_OUT"
        response = self.send_command(command)
        return response

    def set_hdcp_mode(self, prm, prm1):
        """Set HDCP mode
        prm = {0,1,2,3,4}
        // 0: follow source
        // 1: follow sink
        // 2: hdcp disabled
        // 3: hdcp 1.4
        // 4: hdcp 2.2
        prm1 = {0,1,2}
        // 0: hdcp 2.2 + hdcp 1.4
        // 1: hdcp 1.4
        // 2: no hdcp"""
        command = f"SET HDCP_S {prm} {prm1}"
        response = self.send_command(command)
        return response

    def set_edid_mode(self, prm, prm1):
        """Set input EDID mode
        prm = {1,2,3,4}
        // 0: hdmi in 1
        // 1: hdmi in 2
        // 2: hdmi in 3
        // 3: hdmi in 4
        prm1 = {0 ~ x}
        // 0: copy from hdmi out
        // 1: custom EDID"""
        command = f"SET EDID {prm} {prm1}"
        response = self.send_command(command)
        return response

    def get_edid_mode(self, prm):
        """Get input EDID mode
        prm = {1,2,3,4}
        // 0: hdmi in 1
        // 1: hdmi in 2
        // 2: hdmi in 3
        // 3: hdmi in 4
        prm1 = {0 ~ x}
        // 0: copy from hdmi out
        // 1: custom EDID"""
        command = f"GET EDID {prm}"
        response = self.send_command(command)
        return response

    def set_edid_custom(self, prm, prm1, prm2):
        """Write EDID content to input
        Return: EDID_W prm prm1 prm3
        prm = {1,2,3,4}
        // 0: hdmi in 1
        // 1: hdmi in 2
        // 2: hdmi in 3
        // 3: hdmi in 4
        prm1 = {block0, block1}
        prm2 = one block of 256 bytes edid ascii data with no spaces
        prm3 = {ok, error} error= check sum error"""
        command = f"SET EDID_W {prm} {prm1} {prm2}"
        response = self.send_command(command)
        return response

    def get_edid_custom(self, prm, prm1):
        """Get input EDID
        Return: EDID_W prm prm1 prm3
        prm = {1,2,3,4}
        // 0: hdmi in 1
        // 1: hdmi in 2
        // 2: hdmi in 3
        // 3: hdmi in 4
        prm1 = {block0, block1}
        prm2 = one block of 256 bytes edid ascii data with no spaces
        prm3 = {XX...XX} EDID data"""
        command = f"GET EDID_W {prm} {prm1}"
        response = self.send_command(command)
        return response

    def set_layout_pip_positon(self, prm):
        """Sets the location of PIP window
        prm = {0,1,2,3}
        // 0: Top Left
        // 1: Top Right
        // 2: Botton Left
        // 3: Bottom Right"""
        command = f"SET VIDOUT_PIP_POS {prm}"
        response = self.send_command(command)
        return response

    def get_layout_pip_positon(self):
        """get the location of PIP window
        prm = {0,1,2,3}
        // 0: Top Left
        // 1: Top Right
        // 2: Botton Left
        // 3: Bottom Right"""
        command = "GET VIDOUT_PIP_POS"
        response = self.send_command(command)
        return response

    def set_layout_pip_size(self, prm):
        """set the size of the PIP layout
        prm = {0,1,2}
        // 0: 1/4
        // 1: 1/9
        // 2: 1/16"""
        command = f"SET VIDOUT_PIP_SIZE {prm}"
        response = self.send_command(command)
        return response

    def get_layout_pip_size(self):
        """get the size of the PIP layout
        prm = {0,1,2}
        // 0: 1/4
        // 1: 1/9
        // 2: 1/16"""
        command = "GET VIDOUT_PIP_SIZE"
        response = self.send_command(command)
        return response

    def set_cec_power(self, prm):
        """Send CEC power command
        prm = {0,1} // 0: power off, 1: power on"""
        command = f"SET CEC_PWR {prm}"
        response = self.send_command(command)
        return response

    def set_cec_power_auto(self, prm):
        """Set CEC auto power status
        prm = {0,1} // 0: off, 1: on"""
        command = f"SET AUTOCEC_FN {prm}"
        response = self.send_command(command)
        return response

    def get_cec_power_auto(self):
        """Get CEC auto power status
        prm = {0,1} // 0: off, 1: on"""
        command = "GET AUTOCEC_FN"
        response = self.send_command(command)
        return response

    def set_cec_power_delay(self, prm):
        """Set CEC auto power delay
        prm = {1,2,3,...} // minutes"""
        command = f"SET AUTOCEC_D {prm}"
        response = self.send_command(command)
        return response

    def get_cec_power_delay(self):
        """Get CEC auto power delay
        prm = {1,2,3,...} // minutes"""
        command = "GET AUTOCEC_D"
        response = self.send_command(command)
        return response

    def set_uart_power_auto(self, prm):
        """Set UART/RS232 auto power status
        prm = {0,1} // 0: off, 1: on"""
        command = f"SET UARTPWR_FN {prm}"
        response = self.send_command(command)
        return response

    def get_uart_power_auto(self):
        """Get UART/RS232 auto power status
        prm = {0,1} // 0: off, 1: on"""
        command = "GET UARTPWR_FN"
        response = self.send_command(command)
        return response

    def set_uart_command(self, prm, prm1):
        """Set UART/RS232 command
        prm = {0,1} // 0: off, 1: on
        prm1 = {xxxxxxxxxxxxxxxxxx} //PRM2 is the original command+C47:C48 according to device standards
        """
        # TODO not sure how this would work
        command = f"SET UART_STR {prm} {prm1}"
        response = self.send_command(command)
        return response

    def set_uart_command_hex(self, prm, hex1, hex2, hex3):
        """Set UART Hex command
        prm = {0,1} // 0: off, 1: on
        Hex1, hex2 …. = {xx xx xx xx …. }//hex1, hex2…., is asscii string of hex value.
        For example, string "123", convent to correct format string is“31 32 33”."""
        # TODO this will not work in this function, see how to handle x amount of Hex values
        command = f"SET UART_HEX {prm} {hex1} {hex2} {hex3}"
        response = self.send_command(command)
        return response

    def set_uart_power_mode(self, prm):
        """Set UART characters
        prm = {0,1} // 0: string, 1: hex"""
        command = f"SET UART_MODE {prm}"
        response = self.send_command(command)
        return response

    def set_uart_config(self, prm, prm1, prm2, prm3):
        """Set UART configuration settings
        prm = {9600, 19200, 38400, 57600, 115200} Baudrate
        prm1 = {7,8} Databits
        prm2 = {N,O,E}
        // N: No parity
        // O: Odd parity
        // E: Even parity
        prm3 = {1, 1.5, 2}"""
        command = f"SET UART_CFG {prm} {prm1} {prm2} {prm3}"
        response = self.send_command(command)
        return response

    def device_upgrade(self):
        """Enables Upgrade Mode"""
        command = "UPG"
        response = self.send_command(command)
        return response

    def factory_reset(self):
        """Factory Reset Device"""
        command = "RESET"
        response = self.send_command(command)
        return response

    def set_system_ir(self, prm):
        """Set System code for IR"""
        command = f"SET IR_SC {prm}"
        response = self.send_command(command)
        return response

    def get_system_ir(self):
        """Get System code for IR"""
        command = "GET IR_SC"
        response = self.send_command(command)
        return response

    def system_reboot(self):
        """Reboot system"""
        command = "REBOOT"
        response = self.send_command(command)
        return response

    def get_input_video_info(self, prm4):
        """Get video information for input
        Return: VIDIN_INFO prm prm1 prm2
        prm: timing
        prm1: color space
        prm2: color depth
        prm4 = {1,2,3,4}
        // 1: hdmi in 1
        // 2: hdmi in 2
        // 3: hdmi in 3
        // 4: hdmi in 4"""
        command = f"GET VIDIN_INFO {prm4}"
        response = self.send_command(command)
        return response

    def get_input_audio_info(self, prm4):
        """Get audio information for input
        Return: AUDIN_INFO prm prm1 prm2
        prm: format
        prm1: channel
        prm2: sample rate
        prm4 = {1,2,3,4}
        // 1: hdmi in 1
        // 2: hdmi in 2
        // 3: hdmi in 3
        // 4: hdmi in 4"""
        command = f"GET AUDIN_INFO {prm4}"
        response = self.send_command(command)
        return response

    def get_output_video_info(self):
        """Get video output information"""
        command = "GET VIDOUT_INFO"
        response = self.send_command(command)
        return response

    def get_output_audio_info(self, prm3):
        """Get audio output information
        Return: AUDOUT_INFO prm3 prm prm1 prm2
        prm: format
        prm1: channel
        prm2: sample rate
        prm3= {0, 1}  //0 : hdmi out ; 1: av out"""
        command = f"GET AUDOUT_INFO {prm3}"
        response = self.send_command(command)
        return response

    def get_input_signal(self, prm):
        """Get input signal is valid
        Return: VIDIN_VALID prm prm1
        prm4 = {1,2,3,4}
        // 1: hdmi in 1
        // 2: hdmi in 2
        // 3: hdmi in 3
        // 4: hdmi in 4
        prm1 = {0,1} // 0: Not valid, 1: Valid"""
        command = f"GET VIDIN_VALID {prm}"
        response = self.send_command(command)
        return response

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


if __name__ == "__main__":
    device = "/dev/cu.usbserial-A9UK1ODD"
    multiview = MV0401_Device_Serial(device)
    multiview.help()
    multiview.get_firmware_ver()
