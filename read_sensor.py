import RPi.GPIO as GPIO
import time
import spidev

# Enable SPI for communication with sensor
spi_ch = 0
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000


def read_sensor(vref = 3.30):
    
    # Turn on GPIO power: 3.3V on GPIO 22
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.2)

    # Construct SPI message
    # First byte: Only a single start bit (1)
    start_msg = 0b1
    
    # Second byte: SGL/DIFF (single input or diff between ch.)
    #              3 bits for channel (000 = CH0)
    #              rest 0
    setup_msg = 0b1 << 7 # same as 0b10000000
    
    # Third byte: Req. a third byte to get the final byte of the response
    #             Can be anything.
    recieve_msg = 0b00000000
    
    # Sending:    00000001 10000000 00000000
    # Recieving:  //////// /////0ab cdefghij
    # where a-j is bits 9-0 of the signal
    # (abcdefghi in binary representation)
    
    msg = [start_msg, setup_msg, recieve_msg]
    reply = spi.xfer2(msg)
    
    # Construct single integer out of the reply (2 bytes)
    adc = (reply[1] << 8) + reply[2]

    # Calculate voltage from ADC value
    voltage = (vref * (adc+1)) / 1024
    # print(adc, voltage)
    
    # Turn off GPIO power
    GPIO.output(22, GPIO.LOW)

    return voltage