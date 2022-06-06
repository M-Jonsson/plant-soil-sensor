import time
import datetime
import spidev
import RPi.GPIO as GPIO
from read_sensor import read_sensor
import send_email
import log_data

# Time between measurements (minutes)
log_interval = 60

# GPIO control by GPIO number
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT) #GPIO 22 = pin 15 as 3.3V output

GPIO.output(22, GPIO.LOW)
time.sleep(1)

def run():
    # Keep track of last email sent to avoid spamming
    last_email = datetime.datetime.now()
    # 3 last measurements to calculate average
    measurements = [float('nan'), float('nan'), float('nan')]

    while True:
        adc_0 = read_sensor()
        log_data.csv_append('/home/pi/Desktop/soil_moisture/soil_moisture.csv', round(adc_0, 4), plant_id)
        
        # Update latest measurements list
        measurements.insert(0, adc_0)
        measurements.pop()
        print(measurements) #TODO: Delete test print
        if sum(measurements)/3 > 2.5:
            # Calculate time since last email sent
            now = datetime.datetime.now()
            time_diff = now - last_email
            time_diff = time_diff.total_seconds()
            print(sum(measurements)/3) #TODO: Delete test print
            # Send email if during daytime and >10h since last email
            if now.hour >= 8 and now.hour <= 21 and time_diff > 10*3600:
                send_email.send(adc_0)
                last_email = datetime.datetime.now()
                print('Sending email') #TODO: Delete test print

        # Interval converted to seconds, corrected for time to run
        time.sleep(log_interval*60-3)

def init():
    # Assign plant_id='NA' if no id is specified
    plant_id = input('Plant id: ')
    if plant_id == '':
        plant_id = 'NA'

    # Get sender and recipient emails from text file
    with open('emails.txt') as file:
        emails = file.read().split(',')

    return plant_id, emails
    

if __name__ == '__main__':
    # Init id of measured plant and emails
    plant_id, emails = init()

    # Start sensor mearurement
    try:
        run()
    except KeyboardInterrupt:
        print('Stopping measurements')
        GPIO.cleanup()