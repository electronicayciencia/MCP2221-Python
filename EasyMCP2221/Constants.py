DEV_DEFAULT_VID = 0x04D8
DEV_DEFAULT_PID = 0x00DD

PACKET_SIZE = 64
DIR_OUTPUT  = 0
DIR_INPUT   = 1

# Commands
CMD_POLL_STATUS_SET_PARAMETERS    = 0x10
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

RESPONSE_RESULT_OK = 0
RESPONSE_ECHO_BYTE   = 0
RESPONSE_STATUS_BYTE = 1

# Flash data constants
FLASH_DATA_CHIP_SETTINGS          = 0x00
FLASH_DATA_GP_SETTINGS            = 0x01
FLASH_DATA_USB_MANUFACTURER       = 0x02
FLASH_DATA_USB_PRODUCT            = 0x03
FLASH_DATA_USB_SERIALNUM          = 0x04
FLASH_DATA_CHIP_SERIALNUM         = 0x05

# Bytes in Flash Chip Settings register (0-based)
# Write and read are same order but different offsets
FLASH_OFFSET_WRITE = 2
FLASH_OFFSET_READ  = 4

FLASH_CHIP_SETTINGS_CDC_SEC =  2 - 2
FLASH_CHIP_SETTINGS_CLOCK   =  3 - 2
FLASH_CHIP_SETTINGS_DAC     =  4 - 2
FLASH_CHIP_SETTINGS_INT_ADC =  5 - 2
FLASH_CHIP_SETTINGS_LVID    =  6 - 2
FLASH_CHIP_SETTINGS_HVID    =  7 - 2
FLASH_CHIP_SETTINGS_LPID    =  8 - 2
FLASH_CHIP_SETTINGS_HPID    =  9 - 2
FLASH_CHIP_SETTINGS_USBPWR  = 10 - 2
FLASH_CHIP_SETTINGS_USBMA   = 11 - 2
FLASH_CHIP_SETTINGS_PWD1    = 12 - 2
FLASH_CHIP_SETTINGS_PWD2    = 13 - 2
FLASH_CHIP_SETTINGS_PWD3    = 14 - 2
FLASH_CHIP_SETTINGS_PWD4    = 15 - 2
FLASH_CHIP_SETTINGS_PWD5    = 16 - 2
FLASH_CHIP_SETTINGS_PWD6    = 17 - 2
FLASH_CHIP_SETTINGS_PWD7    = 18 - 2
FLASH_CHIP_SETTINGS_PWD8    = 19 - 2

# Bytes in Flash GP Settings register (0-based)
# Write and read are same order but different offsets
FLASH_GP_SETTINGS_GP0       =  2 - 2
FLASH_GP_SETTINGS_GP1       =  3 - 2
FLASH_GP_SETTINGS_GP2       =  4 - 2
FLASH_GP_SETTINGS_GP3       =  5 - 2

# Bytes in Get SRAM Settings response (starting at 0)
SRAM_CHIP_SETTINGS_CDC_SEC  =  4 - 4
SRAM_CHIP_SETTINGS_CLOCK    =  5 - 4
SRAM_CHIP_SETTINGS_DAC      =  6 - 4
SRAM_CHIP_SETTINGS_INT_ADC  =  7 - 4
SRAM_CHIP_SETTINGS_LVID     =  8 - 4
SRAM_CHIP_SETTINGS_HVID     =  9 - 4
SRAM_CHIP_SETTINGS_LPID     = 10 - 4
SRAM_CHIP_SETTINGS_HPID     = 11 - 4
SRAM_CHIP_SETTINGS_USBPWR   = 12 - 4
SRAM_CHIP_SETTINGS_USBMA    = 13 - 4
SRAM_CHIP_SETTINGS_PWD1     = 14 - 4
SRAM_CHIP_SETTINGS_PWD2     = 15 - 4
SRAM_CHIP_SETTINGS_PWD3     = 16 - 4
SRAM_CHIP_SETTINGS_PWD4     = 17 - 4
SRAM_CHIP_SETTINGS_PWD5     = 18 - 4
SRAM_CHIP_SETTINGS_PWD6     = 19 - 4
SRAM_CHIP_SETTINGS_PWD7     = 20 - 4
SRAM_CHIP_SETTINGS_PWD8     = 21 - 4
SRAM_GP_SETTINGS_GP0        = 22 - 4
SRAM_GP_SETTINGS_GP1        = 23 - 4
SRAM_GP_SETTINGS_GP2        = 24 - 4
SRAM_GP_SETTINGS_GP3        = 25 - 4


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
GPIO_FUNC_ADC = GPIO_FUNC_ALT_0
GPIO_FUNC_DAC = GPIO_FUNC_ALT_1


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

I2C_CMD_CANCEL_CURRENT_TRANSFER = 0x10
I2C_CMD_SET_BUS_SPEED = 0x20

RESET_CHIP_SURE           = 0xAB
RESET_CHIP_VERY_SURE      = 0xCD
RESET_CHIP_VERY_VERY_SURE = 0xEF


I2C_CHUNK_SIZE = 60

# For CMD_I2C_READ_DATA_GET_I2C_DATA, I2C READ, etc
# but not for CMD_POLL_STATUS_SET_PARAMETERS.
I2C_INTERNAL_STATUS_BYTE      = 2

# Internal status machine code
# from Microchip's SMBbus driver example
# meaning got by trial and error
I2C_ST_IDLE                   = 0x00
I2C_ST_START                  = 0x10  # sending start condition
I2C_ST_START_ACK              = 0x11
I2C_ST_START_TOUT             = 0x12
I2C_ST_REPSTART               = 0x15
I2C_ST_REPSTART_ACK           = 0x16
I2C_ST_REPSTART_TOUT          = 0x17

I2C_ST_WRADDRL                = 0x20
I2C_ST_WRADDRL_WAITSEND       = 0x21
I2C_ST_WRADDRL_ACK            = 0x22
I2C_ST_WRADDRL_TOUT           = 0x23
I2C_ST_WRADDRL_NACK_STOP_PEND = 0x24
I2C_ST_WRADDRL_NACK_STOP      = 0x25  # device did not ack
I2C_ST_WRADDRH                = 0x30
I2C_ST_WRADDRH_WAITSEND       = 0x31
I2C_ST_WRADDRH_ACK            = 0x32
I2C_ST_WRADDRH_TOUT           = 0x33

I2C_ST_WRITEDATA              = 0x40  # sending data chunk to slave
I2C_ST_WRITEDATA_WAITSEND     = 0x41  # happens sometimes, retry works ok
I2C_ST_WRITEDATA_ACK          = 0x42
I2C_ST_WRITEDATA_WAIT         = 0x43  # waiting for slave to ack after sending a byte
I2C_ST_WRITEDATA_TOUT         = 0x44
I2C_ST_WRITEDATA_END_NOSTOP   = 0x45  # last transfer finished, in non stop mode

I2C_ST_READDATA               = 0x50  # reading data from i2c slave
I2C_ST_READDATA_RCEN          = 0x51
I2C_ST_READDATA_TOUT          = 0x52  # read data timed out
I2C_ST_READDATA_ACK           = 0x53
I2C_ST_READDATA_WAIT          = 0x54  # data buffer is full, more data to come
I2C_ST_READDATA_WAITGET       = 0x55  # data buffer is full, no more data to come

I2C_ST_STOP                   = 0x60
I2C_ST_STOP_WAIT              = 0x61
I2C_ST_STOP_TOUT              = 0x62  # timeout in stop condition (bus busy)

# Bytes in CMD_POLL_STATUS_SET_PARAMETERS response
I2C_POLL_RESP_NEWSPEED_STATUS =  3
I2C_POLL_RESP_STATUS          =  8
I2C_POLL_RESP_REQ_LEN_L       =  9
I2C_POLL_RESP_REQ_LEN_H       = 10
I2C_POLL_RESP_TX_LEN_L        = 11
I2C_POLL_RESP_TX_LEN_H        = 12
I2C_POLL_RESP_CLKDIV          = 14
I2C_POLL_RESP_UNDOCUMENTED_1  = 18
I2C_POLL_RESP_ACK             = 20
I2C_POLL_RESP_SCL             = 22
I2C_POLL_RESP_SDA             = 23
