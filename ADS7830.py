import smbus2 as smbus
class ADS7830:
    # busid - 1 for new Raspberry Pi, 0 for old versions
    # address - I2C address of ADS7830
    def __init__(self, busid, address):
        self._bus = smbus.SMBus(busid)
        self._address = address

    # channel - ADC channel 0-7
    def read(self, channel):
        channelAddress = 0b10000100 | ((channel // 2) if (channel % 2 == 0) else ((channel // 2) + 4)) << 4
        self._bus.write_byte(self._address, channelAddress)
        adcValue = self._bus.read_byte(self._address)
        return adcValue


if __name__ == "__main__":
    ads = ADS7830(1, 0x48)
    for i in range(0,8):
        print("Channel {0}: {1}".format(i, ads.read(i)))