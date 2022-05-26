import csv
import time
import os.path

def init_csv(filename):
    '''
    Initialize a new .csv-file <filename>.
    Checks if the file already exists and asks for \
        confirmation to overwrite if that is the case.
    '''

    header = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Voltage', 'Plant_id']

    if os.path.exists(filename):
        replace = input('File already exists, initialize new file by overwriting? (y/n)')
        if replace.lower() == 'y':
            print('New file initialized by overwriting old version.')
            create_header(filename, header)
        else:
            print('Canceling csv-file initialization.')
    else:
        create_header(filename, header)


def create_header(filename, header):
    '''
    Opens the .csv-file in 'w'-mode clear its contents \
        and then adds the header line.
    '''
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    except:
        print(f'Unable to write to file {filename}')


def csv_append(filename: str, voltage, plant_id):
    '''
    Appends date/time (year, month, day, hour, minute) \
        sensor reading and plant_id to the .csv-file. 
    '''
    with open(filename, 'a', newline='') as file:
        now = time.strftime("%Y,%m,%d,%H,%M", time.localtime())

        writer = csv.writer(file, delimiter=',', quotechar='"')

        row = now.split(',')
        row.extend([voltage, plant_id])

        writer.writerow(row)

# init_csv('/home/pi/Desktop/soil_moisture/soil_moisture.csv')
# csv_append('/home/pi/Desktop/soil_moisture/soil_moisture.csv', 2.7355, 0)