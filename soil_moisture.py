import time
import spidev
import RPi.GPIO as GPIO
from read_sensor import read_sensor
import log_data

# Time between measurements (minutes)
log_interval = 60

# GPIO control by GPIO number
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT) #GPIO 22 = pin 15 as 3.3V output

GPIO.output(22, GPIO.LOW)
time.sleep(1)

def start():
    while True:
        adc_0 = read_sensor()
        log_data.csv_append('/home/pi/Desktop/soil_moisture/soil_moisture.csv', round(adc_0, 4), plant_id)
        time.sleep(log_interval*60)

if __name__ == '__main__':
    # Assign plant_id='NA' if no id is specified
    plant_id = input('Plant id: ')
    if plant_id == '':
        plant_id = 'NA'

    # Start sensor mearurement
    try:
        start()
    except KeyboardInterrupt:
        print('Stopping measurements')
        GPIO.cleanup()  