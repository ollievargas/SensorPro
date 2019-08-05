# Importing modules
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
import urllib
import urllib2


#added code for  sending data to adafruit
aiokey = "1de8b4e601e94f9a96f29c07626470c2"

def getUrl(feed):
  return "https://io.adafruit.com/api/feeds/" + feed + "/data"

headers = {
    'x-aio-key': aiokey,
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 


# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


while True:
  output = analogInput(0) # Reading from CH0
  output = interp(output, [0, 1023], [100, 0])
  output = int(output)
# added code for printing to chart
  moistdata = urllib.urlencode({'value': output})
  req = urllib2.Request(getUrl('moisture'), moistdata, headers)
  response = urllib2.urlopen(req)


  print("Moisture:", output)
  sleep(2.5)
