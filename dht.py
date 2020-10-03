import subprocess
import config
import notification

MAX_TEMPERATURE = config.MAX_TEMPERATURE
MAX_HUMIDITY = config.MAX_HUMIDITY

# Read temperature, humidity from DHT11
data = subprocess.check_output(['dht']).decode()
array = str(data).split('/')

temperature = array[0]
humidity = array[1]

if(float(temperature) > MAX_TEMPERATURE or float(humidity) > MAX_HUMIDITY) :
  notification.send_email('SOAP ROOM ALERT', 'Temperature = ' + str(temperature) + " C / " + 'Humidity = ' + str(MAX_HUMIDITY) + ' %')