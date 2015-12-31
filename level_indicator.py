import spidev
spi = spidev.SpiDev()
class ReedSwitch:
    def __init__(self, CHANNEL):

        #MCP3800 channel associated with this switch
        self.CHANNEL = CHANNEL

    spi.open(0,0)
    
    def readchannel(self):
	adc = spi.xfer2([1,(8+self.CHANNEL)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	volts = (data * 3.3) / float(1023)
  	volts = round(volts,2)
 	return volts
	


