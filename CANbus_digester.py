import csv
import datetime

class CanbusDigester():

    canbus_datasource = None

    def write_line(self, line, record_type = 'csv'):
        if record_type == 'csv':
            split_line = ','.split(line)
            with open('CANbus_outfile.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(split_line)

    def parse_line(self, line):
        split_line = ' '.split(line)
        time_zulu = datetime.utcfromtimestamp(split_line[0]).isoformat()
        data = '#'.split(split_line[2])


    def __init__(self, data_source):


