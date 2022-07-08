#############################################################
#    MIT License                                            #
#    Copyright (c) 2017 Yuta KItagami                       #
#############################################################

import hid
# import hid
# pip install hidapi
# https://github.com/trezor/cython-hidapi
import time
import os

DEV_DEFAULT_VID = 0x04D8
DEV_DEFAULT_PID = 0x00DD

PACKET_SIZE_65 = 65 # for compile_packet function

PACKET_SIZE = 64
DIR_OUTPUT  = 0
DIR_INPUT   = 1

# Commands
CMD_STATUS_SET_PARAMETERS         = 0x10
CMD_SET_GPIO_OUTPUT_VALUES        = 0x50
CMD_GET_GPIO_VALUES               = 0x51
CMD_SET_SRAM_SETTINGS             = 0x60
CMD_GET_SRAM_SETTINGS             = 0x61
CMD_I2C_READ_DATA_GET_I2C_DATA    = 0x40
CMD_I2C_WRITE_DATA                = 0x90
CMD_I2C_READ_DATA                 = 0x91
CMD_I2C_WRITE_DATA_REPEATED_START = 0x92
CMD_I2C_READ_DATA_REPEATED_START  = 0x93
CMD_I2C_WRITE_DATA_NO_STOP        = 0x94
CMD_READ_FLASH_DATA               = 0xB0
CMD_WRITE_FLASH_DATA              = 0xB1
CMD_SEND_FLASH_ACCESS_PASSWORD    = 0xB2
CMD_RESET_CHIP                    = 0x70

CMD_RESULT_OK = 0

# Flash data constants
FLASH_DATA_CHIP_SETTINGS          = 0x00
FLASH_DATA_GP_SETTINGS            = 0x01
FLASH_DATA_USB_MANUFACTURER       = 0x02
FLASH_DATA_USB_PRODUCT            = 0x03
FLASH_DATA_USB_SERIALNUM          = 0x04
FLASH_DATA_CHIP_SERIALNUM         = 0x05

# GPIO constants
GPIO_GP0 = 0
GPIO_GP1 = 1
GPIO_GP2 = 2
GPIO_GP3 = 3

ALTER_GPIO_CONF    = 1 << 7 # bit 7: alters the current GP designation
PRESERVE_GPIO_CONF = 0 << 7
GPIO_OUT_VAL_1  = 1 << 4
GPIO_OUT_VAL_0  = 0 << 4
GPIO_DIR_IN     = 1 << 3
GPIO_DIR_OUT    = 0 << 3
GPIO_FUNC_GPIO  = 0b000
GPIO_FUNC_DEDICATED = 0b001
GPIO_FUNC_ALT_0  = 0b010
GPIO_FUNC_ALT_1  = 0b011
GPIO_FUNC_ALT_2  = 0b100

ALTER_INT_CONF    = 1 << 7 # Enable the modification of the interrupt detection conditions
PRESERVE_INT_CONF = 0 << 7
INT_POS_EDGE_ENABLE  = 0b11 << 3
INT_POS_EDGE_DISABLE = 0b10 << 3
INT_NEG_EDGE_ENABLE  = 0b11 << 1
INT_NEG_EDGE_DISABLE = 0b10 << 1
INT_FLAG_CLEAR    = 1
INT_FLAG_PRESERVE = 0

ALTER_ADC_REF    = 1 << 7 # Enable loading of a new ADC reference
PRESERVE_ADC_REF = 0 << 7
ADC_VRM_OFF  = 0b00 << 1
ADC_VRM_1024 = 0b01 << 1
ADC_VRM_2048 = 0b10 << 1
ADC_VRM_4096 = 0b11 << 1
ADC_REF_VRM  = 1
ADC_REF_VDD  = 0

ALTER_DAC_REF    = 1 << 7 # Enable loading of a new DAC reference
PRESERVE_DAC_REF = 0 << 7
DAC_VRM_OFF  = 0b00 << 1
DAC_VRM_1024 = 0b01 << 1
DAC_VRM_2048 = 0b10 << 1
DAC_VRM_4096 = 0b11 << 1
DAC_REF_VRM  = 1
DAC_REF_VDD  = 0

ALTER_DAC_VALUE    = 1 << 7 # Enable loading of a new DAC value
PRESERVE_DAC_VALUE = 0 << 7

ALTER_CLK_OUTPUT    = 1 << 7 # Enable loading of a new clock divider
PRESERVE_CLK_OUTPUT = 0 << 7
CLK_DUTY_0  = 0b00 << 3
CLK_DUTY_25 = 0b01 << 3
CLK_DUTY_50 = 0b10 << 3
CLK_DUTY_75 = 0b11 << 3
CLK_DIV_1 = 0b001
CLK_DIV_2 = 0b010
CLK_DIV_3 = 0b011
CLK_DIV_4 = 0b100
CLK_DIV_5 = 0b101
CLK_DIV_6 = 0b110
CLK_DIV_7 = 0b111
CLK_FREQ_375kHz = CLK_DIV_7
CLK_FREQ_750kHz = CLK_DIV_6
CLK_FREQ_1_5MHz = CLK_DIV_5
CLK_FREQ_3MHz   = CLK_DIV_4
CLK_FREQ_6MHz   = CLK_DIV_3
CLK_FREQ_12MHz  = CLK_DIV_2
CLK_FREQ_24MHz  = CLK_DIV_1



class PyMCP2221A:
    def __init__(self, VID = DEV_DEFAULT_VID, PID = DEV_DEFAULT_PID, devnum=0):
        self.CLKDUTY_0  = 0x00
        self.CLKDUTY_25 = 0x08
        self.CLKDUTY_50 = 0x10
        self.CLKDUTY_75 = 0x18

        # self.CLKDIV_1 = 0x00    # 48MHz  Dont work.
        self.CLKDIV_2   = 0x01  # 24MHz
        self.CLKDIV_4   = 0x02  # 12MHz
        self.CLKDIV_8   = 0x03  # 6MHz
        self.CLKDIV_16  = 0x04  # 3MHz
        self.CLKDIV_32  = 0x05  # 1.5MHz
        self.CLKDIV_64  = 0x06  # 750KHz
        self.CLKDIV_128 = 0x07  # 375KHz

        self.mcp2221a = hid.device()
        self.mcp2221a.open_path(hid.enumerate(VID, PID)[devnum]["path"])


    # Obsolete
    def compile_packet(self, buf):
        """
        :param list buf:
        """
        assert len(buf) <= PACKET_SIZE_65

        buf = buf + [0 for i in range(PACKET_SIZE_65 - len(buf))]
        return buf


    def send_cmd(self, buf):
        REPORT_NUM = 0x00
        padding = [0x00] * (PACKET_SIZE - len(buf))
        self.mcp2221a.write([REPORT_NUM] + buf + padding)

        if buf[0] == CMD_RESET_CHIP:
            return none
        else:
            return self.mcp2221a.read(PACKET_SIZE)


    #######################################################################
    # HID DeviceDriver Info
    #######################################################################
    def DeviceDriverInfo(self):
        print("Manufacturer: %s" % self.mcp2221a.get_manufacturer_string())
        print("Product: %s" % self.mcp2221a.get_product_string())
        print("Serial No: %s" % self.mcp2221a.get_serial_number_string())

    #######################################################################
    # Command Structure
    #######################################################################
    def Command_Structure(self, I2C_Cancel_Bit, I2C_Speed_SetUp_Bit, I2C_Speed_SetVal_Byte):
        I2C_Cancel_Bit = 0
        I2C_Speed_SetUp_Bit = 0
        I2C_Speed_SetVal_Byte = 0
        buf = self.compile_packet([0x00, CMD_STATUS_SET_PARAMETERS, 0x00,
                                   I2C_Cancel_Bit << 4,
                                   I2C_Speed_SetUp_Bit << 5,
                                   I2C_Speed_SetVal_Byte])

        self.mcp2221a.write(buf)
        buf = self.mcp2221a.read(PACKET_SIZE_65)

        print(chr(buf[46]))
        print(chr(buf[47]))
        print(chr(buf[48]))
        print(chr(buf[49]))

    #######################################################################
    # Read Flash Data
    #######################################################################

    def Read_Flash_Data(self):

        CHIP_SETTINGS_STR   = "Chip settings"
        GP_SETTINGS_STR     = "GP settings"
        USB_VENDOR_STR      = "USB Manufacturer"
        USB_PRODUCT_STR     = "USB Product"
        USB_SERIAL_STR      = "USB Serial"
        USB_FACT_SERIAL_STR = "Factory Serial"

        data = {
            CHIP_SETTINGS_STR:    self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_CHIP_SETTINGS]),
            GP_SETTINGS_STR:      self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_GP_SETTINGS]),
            USB_VENDOR_STR:       self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_USB_MANUFACTURER]),
            USB_PRODUCT_STR:      self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_USB_PRODUCT]),
            USB_SERIAL_STR:       self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_USB_SERIALNUM]),
            USB_FACT_SERIAL_STR:  self.send_cmd([CMD_READ_FLASH_DATA, FLASH_DATA_CHIP_SERIALNUM]),
        }

        data[USB_VENDOR_STR]      = self.parse_wchar_structure(data[USB_VENDOR_STR])
        data[USB_PRODUCT_STR]     = self.parse_wchar_structure(data[USB_PRODUCT_STR])
        data[USB_SERIAL_STR]      = self.parse_wchar_structure(data[USB_SERIAL_STR])
        data[USB_FACT_SERIAL_STR] = self.parse_factory_serial(data[USB_FACT_SERIAL_STR])
        data[CHIP_SETTINGS_STR]   = self.parse_chip_settings_struct(data[CHIP_SETTINGS_STR])
        data[GP_SETTINGS_STR]     = self.parse_gp_settings_struct(data[GP_SETTINGS_STR])

        return data

    def parse_wchar_structure(self, buf):
        cmd_echo  = buf[0]
        cmd_error = buf[1]
        strlen    = buf[2] - 2
        three     = buf[3]
        w_str     = buf[4:4+strlen]
        str = bytes(w_str).decode('utf-16')
        return str

    def parse_factory_serial(self, buf):
        cmd_echo  = buf[0]
        cmd_error = buf[1]
        strlen    = buf[2]
        three     = buf[3]
        str       = buf[4:4+strlen]
        str = bytes(str).decode('ascii')
        return str

    def parse_chip_settings_struct(self, buf):
        data = {
            "USB VID": "0x{:02X}{:02X}".format(buf[9], buf[8]),
            "USB PID": "0x{:02X}{:02X}".format(buf[11], buf[10]) ,
            "USB requested number of mA": buf[13] * 2,
            "raw": buf[0:14],
        }
        return data

    def parse_gp_settings_struct(self, buf):
        data = {
            "raw": buf[0:7]
        }
        return data


   #######################################################################
    # Write Flash Data
    #######################################################################

    def Write_Flash_Data(self, data):
        pass
        # Write_Deta_Setting_Byte = 0x00
        # Write_Chip_Settings             = 0x00
        # Write_GP_Settings               = 0x01
        # Write_USB_Manufacturer_Settings = 0x02
        # Write_USB_Product_Settings      = 0x03
        # Write_USB_SerialNum_Settings    = 0x04
        # buf = [0x00,0xB1,Write_Deta_Setting_Byte]
        # buf = buf + [0 for i in range(PACKET_SIZE_65-len(buf))]
        # !!!! Be careful when making changes !!!!
        # buf[6+1] =  0xD8    # VID (Lower)
        # buf[7+1] =  0x04    # VID (Higher)
        # buf[8+1] =  0xDD    # PID (Lower)
        # buf[9+1] =  0x00    # PID (Higher)

        # print ("Write")
        # print (buf)
        # h.write(buf)
        # buf = h.read(PACKET_SIZE_65)
        # print ("Read")
        # print (buf)

    def GPIO_Config(self,
        clk_output = None,
        dac_ref    = None,
        dac_value  = None,
        adc_ref    = None,
        int_conf   = None,
        gp0        = None,
        gp1        = None,
        gp2        = None,
        gp3        = None):
        """ Configure Runtime GPIO pins and parameters. """

        if clk_output is not None: clk_output |= ALTER_CLK_OUTPUT
        if dac_ref    is not None: dac_ref    |= ALTER_DAC_REF
        if dac_value  is not None: dac_value  |= ALTER_DAC_VALUE
        if adc_ref    is not None: adc_ref    |= ALTER_ADC_REF
        if int_conf   is not None: int_conf   |= ALTER_INT_CONF

        new_gpconf = None
        if (gp0, gp1, gp2, gp3) != (None, None, None, None):
            new_gpconf = ALTER_GPIO_CONF
            # Preserve GPx for non specified pins
            status = self.send_cmd([CMD_GET_SRAM_SETTINGS])
            if gp0 is None: gp0 = status[22]
            if gp1 is None: gp1 = status[23]
            if gp2 is None: gp2 = status[24]
            if gp3 is None: gp3 = status[25]

        cmd = [0] * 12
        cmd[0]  = CMD_SET_SRAM_SETTINGS
        cmd[1]  = 0   # don't care
        cmd[2]  = clk_output or PRESERVE_CLK_OUTPUT # Clock Output Divider value
        cmd[3]  = dac_ref    or PRESERVE_DAC_REF    # DAC Voltage Reference
        cmd[4]  = dac_value  or PRESERVE_DAC_VALUE  # Set DAC output value
        cmd[5]  = adc_ref    or PRESERVE_ADC_REF    # ADC Voltage Reference
        cmd[6]  = int_conf   or PRESERVE_INT_CONF   # Setup the interrupt detection
        cmd[7]  = new_gpconf or PRESERVE_GPIO_CONF  # Alter GPIO configuration
        cmd[8]  = gp0        or PRESERVE_GPIO_CONF  # GP0 settings
        cmd[9]  = gp1        or PRESERVE_GPIO_CONF  # GP1 settings
        cmd[10] = gp2        or PRESERVE_GPIO_CONF  # GP2 settings
        cmd[11] = gp3        or PRESERVE_GPIO_CONF  # GP3 settings

        self.send_cmd(cmd)


    #######################################################################
    # GPIO commands
    #######################################################################
    def GPIO_FastSetAsInput(self,
        gp0 = None,
        gp1 = None,
        gp2 = None,
        gp3 = None):
        """
        Define a pin as an input but not writes to SRAM.
        Any call to GPIO_Conf to configure any other pins will reset this settings.
        """

        ALTER_DIRECTION = 1
        PRESERVE_DIRECTION = 0
        GPIO_ERROR = 0xEE

        buf = [0] * 18
        buf[0]  = CMD_SET_GPIO_OUTPUT_VALUES
        buf[4]  = PRESERVE_DIRECTION if gp0 is None else ALTER_DIRECTION
        buf[5]  = gp0 or 0
        buf[8]  = PRESERVE_DIRECTION if gp1 is None else ALTER_DIRECTION
        buf[9]  = gp1 or 0
        buf[12] = PRESERVE_DIRECTION if gp2 is None else ALTER_DIRECTION
        buf[13] = gp2 or 0
        buf[16] = PRESERVE_DIRECTION if gp3 is None else ALTER_DIRECTION
        buf[17] = gp3 or 0

        r = self.send_cmd(buf)

        if gp0 is not None and r[4] == GPIO_ERROR:
            raise RuntimeError("Pin GP0 is not assigned to GPIO function.")
        elif gp1 is not None and r[8] == GPIO_ERROR:
            raise RuntimeError("Pin GP1 is not assigned to GPIO function.")
        elif gp2 is not None and r[12] == GPIO_ERROR:
            raise RuntimeError("Pin GP2 is not assigned to GPIO function.")
        elif gp3 is not None and r[16] == GPIO_ERROR:
            raise RuntimeError("Pin GP3 is not assigned to GPIO function.")


    def GPIO_FastSetValue(self,
        gp0 = None,
        gp1 = None,
        gp2 = None,
        gp3 = None):
        """
        Set pin output values but not write it to SRAM.
        Any call to GPIO_Conf to configure any other pins will reset this settings.
        """

        ALTER_VALUE = 1
        PRESERVE_VALUE = 0
        GPIO_ERROR = 0xEE

        buf = [0] * 18
        buf[0]  = CMD_SET_GPIO_OUTPUT_VALUES
        buf[2]  = PRESERVE_VALUE if gp0 is None else ALTER_VALUE
        buf[3]  = gp0 or 0
        buf[6]  = PRESERVE_VALUE if gp1 is None else ALTER_VALUE
        buf[7]  = gp1 or 0
        buf[10] = PRESERVE_VALUE if gp2 is None else ALTER_VALUE
        buf[11] = gp2 or 0
        buf[14] = PRESERVE_VALUE if gp3 is None else ALTER_VALUE
        buf[15] = gp3 or 0

        r = self.send_cmd(buf)

        if gp0 is not None and r[3] == GPIO_ERROR:
            raise RuntimeError("Pin GP0 is not assigned to GPIO function.")
        elif gp1 is not None and r[7] == GPIO_ERROR:
            raise RuntimeError("Pin GP1 is not assigned to GPIO function.")
        elif gp2 is not None and r[11] == GPIO_ERROR:
            raise RuntimeError("Pin GP2 is not assigned to GPIO function.")
        elif gp3 is not None and r[15] == GPIO_ERROR:
            raise RuntimeError("Pin GP3 is not assigned to GPIO function.")


    def GPIO_Read(self):
        """ Read all GPIO pins and return a tuple (gp0, gp1, gp2, gp3).
        Value is None if that pin is not set for GPIO operation. """

        r = self.send_cmd([CMD_GET_GPIO_VALUES])
        gp0 = r[2] if r[2] != 0xEE else None
        gp1 = r[4] if r[4] != 0xEE else None
        gp2 = r[6] if r[6] != 0xEE else None
        gp3 = r[8] if r[8] != 0xEE else None

        return (gp0, gp1, gp2, gp3)


    def Clock_Config(self, duty, freq):
        """
        Configure the clock output.
        Duty valid values are 0, 25, 50, 75.
        Freq is one of 375kHz, 750kHz, 1.5MHz, 3MHz, 6MHz, 12MHz or 24MHz.
        To output clock signal, you also need to set GP1 function to GPIO_FUNC_DEDICATED.
        """
        if duty == 0:
            duty = CLK_DUTY_0
        elif duty == 25:
            duty = CLK_DUTY_25
        elif duty == 50:
            duty = CLK_DUTY_50
        elif duty == 75:
            duty = CLK_DUTY_75
        else:
            raise ValueError("Accepted values for duty are 0, 25, 50, 75.")

        if freq == "375kHz":
            div = CLK_FREQ_375kHz
        elif freq == "750kHz":
            div = CLK_FREQ_750kHz
        elif freq == "1.5MHz":
            div = CLK_FREQ_1_5MHz
        elif freq == "3MHz":
            div = CLK_FREQ_3MHz
        elif freq == "6MHz":
            div = CLK_FREQ_6MHz
        elif freq == "12MHz":
            div = CLK_FREQ_12MHz
        elif freq == "24MHz":
            div = CLK_FREQ_24MHz
        else:
            raise ValueError("Freq is one of 375kHz, 750kHz, 1.5MHz, 3MHz, 6MHz, 12MHz or 24MHz")

        self.GPIO_Config(clk_output = duty | div)


    #######################################################################
    # ADC 1
    #######################################################################
    def ADC_1_Init(self):
        buf = self.compile_packet([0x00, CMD_GET_SRAM_SETTINGS])
        self.mcp2221a.write(buf)

        rbuf = self.mcp2221a.read(PACKET_SIZE_65)

        buf = self.compile_packet([0x00, CMD_SET_SRAM_SETTINGS])
        buf[2 + 1] = rbuf[5]  # Clock Output Divider value
        buf[3 + 1] = rbuf[6]  # DAC Voltage Reference
        buf[4 + 1] = 0x00  # Set DAC output value
        buf[5 + 1] = 0x00  # ADC Voltage Reference
        buf[6 + 1] = 0x00  # Setup the interrupt detection mechanism and clear the detection flag
        buf[7 + 1] = 0xFF  # Alter GPIO configuration: alters the current GP designation
        #   datasheet says this should be 1, but should actually be 0x80
        buf[8 + 1] = rbuf[22]  # GP0 settings
        buf[9 + 1] = 0x02  # GP1 settings
        buf[10 + 1] = rbuf[24]  # GP2 settings
        buf[11 + 1] = rbuf[25]  # GP3 settings
        self.mcp2221a.write(buf)
        buf = self.mcp2221a.read(PACKET_SIZE_65)

    #######################################################################
    # ADC 2
    #######################################################################

    def ADC_2_Init(self):
        buf = self.compile_packet([0x00, CMD_GET_SRAM_SETTINGS])
        self.mcp2221a.write(buf)

        rbuf = self.mcp2221a.read(PACKET_SIZE_65)

        buf = self.compile_packet([0x00, CMD_SET_SRAM_SETTINGS])
        buf[2 + 1] = rbuf[5]  # Clock Output Divider value
        buf[3 + 1] = rbuf[6]  # DAC Voltage Reference
        buf[4 + 1] = 0x00  # Set DAC output value
        buf[5 + 1] = rbuf[7]  # ADC Voltage Reference
        buf[6 + 1] = 0x00  # Setup the interrupt detection mechanism and clear the detection flag
        buf[7 + 1] = 0x80  # Alter GPIO configuration: alters the current GP designation
        #   datasheet says this should be 1, but should actually be 0x80
        buf[8 + 1] = rbuf[22]  # GP0 settings
        buf[9 + 1] = rbuf[23]  # GP1 settings
        buf[10 + 1] = 0x02  # GP2 settings
        buf[11 + 1] = rbuf[25]  # GP3 settings
        self.mcp2221a.write(buf)
        buf = self.mcp2221a.read(PACKET_SIZE_65)

    #######################################################################
    # ADC 3
    #######################################################################

    def ADC_3_Init(self):
        buf = self.compile_packet([0x00, CMD_GET_SRAM_SETTINGS])

        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(PACKET_SIZE_65)

        buf = self.compile_packet([0x00, CMD_SET_SRAM_SETTINGS])
        buf[2 + 1] = rbuf[5]  # Clock Output Divider value
        buf[3 + 1] = rbuf[6]  # DAC Voltage Reference
        buf[4 + 1] = 0x00  # Set DAC output value
        buf[5 + 1] = rbuf[7]  # ADC Voltage Reference
        buf[6 + 1] = 0x00  # Setup the interrupt detection mechanism and clear the detection flag
        buf[7 + 1] = 0x80  # Alter GPIO configuration: alters the current GP designation
        #   datasheet says this should be 1, but should actually be 0x80
        buf[8 + 1] = rbuf[22]  # GP0 settings
        buf[9 + 1] = rbuf[23]  # GP1 settings
        buf[10 + 1] = rbuf[24]  # GP2 settings
        buf[11 + 1] = 0x02  # GP3 settings
        self.mcp2221a.write(buf)
        buf = self.mcp2221a.read(PACKET_SIZE_65)

    #######################################################################
    # ADC Deta Get
    #######################################################################

    def ADC_DataRead(self):
        buf = self.compile_packet([0x00, CMD_STATUS_SET_PARAMETERS])
        self.mcp2221a.write(buf)

        buf = self.mcp2221a.read(PACKET_SIZE_65)
        # for i in range(len(buf)):
        #    print ("[%d]: 0x{:02x}".format(buf[i]) % (i))
        self.ADC_1_data = buf[50] | (buf[51] << 8)  # ADC Data (16-bit) values
        self.ADC_2_data = buf[52] | (buf[53] << 8)  # ADC Data (16-bit) values
        self.ADC_3_data = buf[54] | (buf[55] << 8)  # ADC Data (16-bit) values

    #######################################################################
    # DAC 1
    #######################################################################
    def DAC_Config(self, ref, out = 0):
        """
        Configure DAC reference.
        ref valid values are "0", "1.024V", "2.048V", "4.096V" and "VDD".
        out valid values are from 0 to 31.
        To output DAC, you also need to set GP2/3 function to GPIO_FUNC_ALT_1.
        """
        if ref == "OFF":
            ref = DAC_REF_VRM
            vrm = DAC_VRM_OFF
        elif ref == "1.024V":
            ref = DAC_REF_VRM
            vrm = DAC_VRM_1024
        elif ref == "2.048V":
            ref = DAC_REF_VRM
            vrm = DAC_VRM_2048
        elif ref == "4.096V":
            ref = DAC_REF_VRM
            vrm = DAC_VRM_4096
        elif ref == "VDD":
            ref = DAC_REF_VDD
            vrm = DAC_VRM_OFF
        else:
            raise ValueError("Accepted values for ref are 'OFF', '1.024V', '2.048V', '4.096V' and 'VDD'.")

        if out < 0 or out > 31:
            raise ValueError("Accepted values for out are from 0 to 31.")

        self.GPIO_Config(
            dac_ref = ref | vrm,
            dac_value = out)


    def DAC_Out(self, out):
        """
        Configure DAC output.
        out valid values are from 0 to 31.
        To output DAC, you also need to set GP2/3 function to GPIO_FUNC_ALT_1.
        """

        if out < 0 or out > 31:
            raise ValueError("Accepted values for out are from 0 to 31.")

        self.GPIO_Config(dac_value = out)


    #######################################################################
    # DAC Output
    #######################################################################

    def DAC_Datawrite(self, value):
        buf = self.compile_packet([0x00, CMD_GET_SRAM_SETTINGS])
        self.mcp2221a.write(buf)

        rbuf = self.mcp2221a.read(PACKET_SIZE_65)

        buf = self.compile_packet([0x00, CMD_SET_SRAM_SETTINGS])
        buf[2 + 1] = rbuf[5]  # Clock Output Divider value
        buf[3 + 1] = 0x00  # DAC Voltage Reference
        buf[4 + 1] = 0x80 | (0x1F & value)  # Set DAC output value
        buf[5 + 1] = rbuf[7]  # ADC Voltage Reference
        buf[6 + 1] = 0x00  # Setup the interrupt detection mechanism and clear the detection flag
        buf[7 + 1] = 0xFF  # Alter GPIO configuration: alters the current GP designation
        #   datasheet says this should be 1, but should actually be 0x80
        buf[8 + 1] = rbuf[22]  # GP0 settings
        buf[9 + 1] = rbuf[23]  # GP1 settings
        buf[10 + 1] = rbuf[24]  # GP2 settings
        buf[11 + 1] = rbuf[25]  # GP3 settings
        self.mcp2221a.write(buf)
        buf = self.mcp2221a.read(PACKET_SIZE_65)

    #######################################################################
    # I2C Init
    #######################################################################
    def I2C_Init(self, speed=100000):  # speed = 100000
        self.MCP2221_I2C_SLEEP = float(os.environ.get("MCP2221_I2C_SLEEP", 0))

        buf = self.compile_packet([0x00, CMD_STATUS_SET_PARAMETERS])
        buf[2 + 1] = 0x00  # Cancel current I2C/SMBus transfer (sub-command)
        buf[3 + 1] = 0x20  # Set I2C/SMBus communication speed (sub-command)
        # The I2C/SMBus system clock divider that will be used to establish the communication speed
        buf[4 + 1] = int((12000000 / speed) - 3)
        self.mcp2221a.write(buf)

        rbuf = self.mcp2221a.read(PACKET_SIZE_65)
        # print("Init")
        if (rbuf[22] == 0):
            raise RuntimeError("SCL is low.")
        if (rbuf[23] == 0):
            raise RuntimeError("SDA is low.")

        # time.sleep(0.001)

    #######################################################################
    # I2C State Check
    #######################################################################
    def I2C_State_Check(self):
        buf = self.compile_packet([0x00, CMD_STATUS_SET_PARAMETERS])
        self.mcp2221a.write(buf)

        rbuf = self.mcp2221a.read(PACKET_SIZE_65)
        return rbuf[8]

    #######################################################################
    # I2C Cancel
    #######################################################################

    def I2C_Cancel(self):
        buf = self.compile_packet([0x00, CMD_STATUS_SET_PARAMETERS])
        buf[2 + 1] = 0x10  # Cancel current I2C/SMBus transfer (sub-command)
        self.mcp2221a.write(buf)

        self.mcp2221a.read(PACKET_SIZE_65)
        # time.sleep(0.1)

    #######################################################################
    # I2C Write
    #######################################################################
    def I2C_Write(self, addrs, data):
        """ Writes a block of data with Start and Stop c condition on bus
        :param int addrs: 7-bit I2C slave address
        :param list data: list of int

        Referring to MCP2221A Datasheet(Rev.B 2017), section 3.1.5
        """
        buf = self.compile_packet([0x00, CMD_I2C_WRITE_DATA])
        self._i2c_write(addrs, data, buf)

    def I2C_Write_Repeated(self, addrs, data):
        """ Writes a block of data with Repeated Start and Stop conditions on bus
        :param int addrs: 7-bit I2C slave address
        :param list data: list of int

        Referring to MCP2221A Datasheet(Rev.B 2017), section 3.1.6
        """
        buf = self.compile_packet([0x00, CMD_I2C_WRITE_DATA_REPEATED_START])
        self._i2c_write(addrs, data, buf)

    def I2C_Write_No_Stop(self, addrs, data):
        """ Writes a block of data with Start condition on bus
        :param int addrs: 7-bit I2C slave address
        :param list data: list of int

        Referring to MCP2221A Datasheet(Rev.B 2017), section 3.1.7
        """
        buf = self.compile_packet([0x00, CMD_I2C_WRITE_DATA_NO_STOP])
        self._i2c_write(addrs, data, buf)

    def _i2c_write(self, addrs, data, buf):

        buf[1 + 1] = (len(data) & 0x00FF)  # Cancel current I2C/SMBus transfer (sub-command)
        buf[2 + 1] = (len(data) & 0xFF00) >> 8  # Set I2C/SMBus communication speed (sub-command)
        # The I2C/SMBus system clock divider that will be used to establish the communication speed
        buf[3 + 1] = 0xFF & (addrs << 1)
        for i in range(len(data)):
            # print ("{:d}: 0x{:02x}".format(i,data[i]))
            buf[4 + 1 + i] = data[
                i]  # The I2C/SMBus system clock divider that will be used to establish the communication speed
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(PACKET_SIZE_65)
        time.sleep(0.008)

    #######################################################################
    # I2C Read
    #######################################################################
    def I2C_Read(self, addrs, size):
        """ Reads a block of data with Start and Stop conditions on bus
        :param int addrs: 7-bit I2C slave address
        :param int size: size of read out in bytes

        Referring to MCP2221A Datasheet(Rev.B 2017), section 3.1.8
        """
        buf = self.compile_packet([0x00, CMD_I2C_READ_DATA])
        return self._i2c_read(addrs, size, buf)

    def I2C_Read_Repeated(self, addrs, size):
        """ Reads a block of data with Repeated Start and Stop conditions on bus
        :param int addrs: 7-bit I2C slave address
        :param int size: size of read out in bytes

        Referring to MCP2221A Datasheet(Rev.B 2017), section 3.1.9
        """
        buf = self.compile_packet([0x00, CMD_I2C_READ_DATA_REPEATED_START])
        return self._i2c_read(addrs, size, buf)

    def _i2c_read(self, addrs, size, buf):

        buf[1 + 1] = (size & 0x00FF)  # Read LEN
        buf[2 + 1] = (size & 0xFF00) >> 8  # Read LEN
        buf[3 + 1] = 0xFF & (addrs << 1)  # addrs
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(PACKET_SIZE_65)
        if (rbuf[1] != 0x00):
            # print("[0x91:0x{:02x},0x{:02x},0x{:02x}]".format(rbuf[1],rbuf[2],rbuf[3]))
            self.I2C_Cancel()
            self.I2C_Init()
            raise RuntimeError("I2C Read Data Failed: Code " + rbuf[1])
        time.sleep(self.MCP2221_I2C_SLEEP)

        buf = self.compile_packet([0x00, 0x40])
        buf[1 + 1] = 0x00
        buf[2 + 1] = 0x00
        buf[3 + 1] = 0x00
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(PACKET_SIZE_65)
        if (rbuf[1] != 0x00):
            # print("[0x40:0x{:02x},0x{:02x},0x{:02x}]".format(rbuf[1],rbuf[2],rbuf[3]))
            self.I2C_Cancel()
            self.I2C_Init()
            print("You can try increasing environment variable MCP2221_I2C_SLEEP")
            raise RuntimeError("I2C Read Data - Get I2C Data Failed: Code " + rbuf[1])
        if (rbuf[2] == 0x00 and rbuf[3] == 0x00):
            self.I2C_Cancel()
            self.I2C_Init()
            return rbuf[4]
        if (rbuf[2] == 0x55 and rbuf[3] == size):
            rdata = [0] * size
            for i in range(size):
                rdata[i] = rbuf[4 + i]
            return rdata

    #######################################################################
    # reset
    #######################################################################
    def Reset(self):
        print("Reset")
        buf = self.compile_packet([0x00, CMD_RESET_CHIP, 0xAB, 0xCD, 0xEF])

        self.mcp2221a.write(buf)
        time.sleep(1)
