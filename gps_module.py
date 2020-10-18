import serial
import csv


class GpsModule():
    port = 'COM3'

    latitude = 0.
    lat_hemisphere = ''
    longitude = 0.
    long_hemisphere = ''
    altitude = 0.
    geoid_height = 0.
    velocity = 0
    heading = 0

    def decode_gpgga(self, data):
        self.latitude = float(data[2])
        self.lat_hemisphere = data[3]
        self.longitude = float(data[4])
        self.long_hemisphere = data[5]
        self.altitude = float(data[9])
        self.geoid_height = float(data[11])

    def decode_gprmc(self, data):
        self.latitude = float(data[3])
        self.lat_hemisphere = data[4]
        self.longitude = float(data[5])
        self.long_hemisphere = data[6]
        self.velocity = float(data[7])
        self.heading = float(data[8])

    def update_data(self):
        data = self.sp.readline().decode('utf8')
        data = data.split(',')
        if data[0] == '$GPGGA':
            self.decode_gpgga(data)
        elif data[0] == '$GPRMC':
            self.decode_gprmc(data)
        elif data[0] in ['$GPGSA', '$GPGSV']:
            pass
        else:
            with open('gps_log.txt', 'a') as fp:
                fp.write("Unkown NMEA code received : %s\n" % data[0])

    def __init__(self):
        self.sp = serial.Serial(self.port, 4800)
        self.update_data()


# def test():
#     lines = []
#
#     while True:
#         msg = sp.readline().decode('utf8')
#         lines.append(msg)
#         with open('gps.csv', 'a', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile, delimiter=',')
#             writer.writerow(msg.split(','))
#         print(msg)
