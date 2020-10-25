# vehicle_assistant

Work on this project is in very early stages, and this document serves more as a scoping document than as a description of the existing state of the software. 

This project intends to display the video captured by a dashcam overlaid with data from both the CANbus connection in a Toyota Prius Mk3 and a connected GPS device. 

Snapshots of this data are to be sent periodically to a central server by MQTT via a 3G connection, providing location and diagnostic data to the home base. 

## Hardware requirements

The software is designed to run with the following hardware:

-  Raspberry Pi 3 Single-board computer*
-  BU-353 S4 USB GPS module
-  PiCAN 2
-  Raspberry Pi camera module v2

* It is also planned to try this software on the Jetson Nano which may involve some modifications

## Software design

Three separate programs are intended. 

### Display module

The first acts as the display component, using OpenCV to display the video captured from the attached camera module. 

Overlaid on the camera output are various data points captiured from the other programs. 

These include:

-  Vehicle velocity reported by CANbus
-  Vehicle velocity reported by the GPS module
-  Direction of travel as reported by the GPS module
-  Lat / Long 
-  Current fuel consumption as reported by CANbus
-  Timestamp

### GPS module

The next takes updates from the GPS module over serial and updates a local instance of MongoDB with each line received.

The NMEA specification allows for various sentences to be constructed, each of which deals with a different function of the GPS module.

Here we are mainly concerned with the following:

-  $GPRMC - Recommended minimum specific GPS/Transit data
-  $GPGGA - Global Positioning System Fix Data

Other sentences are discarded as they don't provide information that we need for our purposes, though this may change in time. 

More information can be found here: 

http://aprs.gids.nl/nmea/

### CANbus module

This module will continuously read from the PiCAN module on the Raspberry Pi. 

This will also update a local DB with data, but there has to be thought givec as to the frequency of the updates as the data rate on CANbus is far higher than required by our project. 

The chances are that we can update only every second or 500ms but this can be played by ear. 

It will also be the case that we won't update with *all* the data that CANbus relays, as only some of it is of interest. 

It is also a sizeable project to identify what data reported relates to what, as there is no officially published information on what CANbus codes relate to what data and these codes are not necessarily consistent even among manufacturers. 

There is therefore an inherent limitation as to what vehicles this software will be compatible with, and in the first instance this will be designed only to work with the 2013 Toyota Prius. 


### Dependencies

```python-can```

https://python-can.readthedocs.io/en/master/index.html





