# vehicle_assistant

Work on this project is in very early stages, and this document serves more as a scoping document than as a description of the existing state of the software. 

This project intends to display the video captured by a dashcam overlaid with data from both the CANbus connection in a Toyota Prius Mk3 and a connected GPS device. 

Snapshots of this data are to be sent periodically to a central server by MQTT via a 3G connection, providing location and diagnostic data to the home base. 

## Hardware requirements

The software is designed to run with the following hardware:

-  Raspberry Pi 3 Single-board computer* **
-  BU-353 S4 USB GPS module
-  PiCAN 2
-  Raspberry Pi camera module v2

* It is also planned to try this software on the Jetson Nano which may involve some modifications
** We are limited here to a Raspberry Pi 3 as the PiCAN 2 is not compatible with the Raspberry Pi 4

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


### Software Setup

#### Operating system and supporting software

The first thing to note is that at the time of writing there appears to be a problem with the latest version of mongodb running on 32-bit Raspberry Pi OS (formerly Raspbian). 

There is an error with the sockets whereby pymongo is not able to communicate with the socket as the correct socket version is not reported by the mongodb server. This error has not been fixed until version 3.2 of mongodb, but mongodb 3.2 was never compiled for 32-bit ARM. 

There is a beta version of a 64-bit Raspberry Pi OS available however, which although limited in some respects does not seem to impact on our requirements: https://www.raspberrypi.org/forums/viewtopic.php?f=117&t=275370


Step 0 - As a matter of course:

```sudo apt-get update```

```sudo apt-get upgrade```


Step 1 - VNC:

Note that although the docs state that VNC cannot be run on the new OS (indeed it does not work if you simply activate it through raspi-config) you can install realvnc-vnc-server from apt-get then activate through config later. 

```sudo apt-get install realvnc-vnc-server```

```sudo systemctl start vncserver-virtuald.service```

```sudo systemctl enable vncserver-virtuald.service```

```sudo raspi-config``` and select "Interface Options" then "VNC" and set to on (It's worth setting Camera and SSH to on at this point also)


Step 2 - resolve wifi issues: 

It was also noticed that the wifi was soft-blocked on second startup. As the vehicle has been parked outside the house (in wifi range!) for testing, this is an issue for us so we needed to fix it. 

It isn't verified at this stage as to whether or not this is an issue with the distro of Raspberry Pi OS or the results of subsequent fooling around, but just in case the solution is listed here:


```rfkill unblock wifi```
```sudo ifconfig wlan0 up```


Step 3 - mongodb:

Now let's get mongo installed. This isn't, at the time of writing, the most succinct of tasks but it works. 

We first need to add the add the key for the mongodb servers to apt:

```curl -s https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -```

Then we add the mongodb servers to apt's sources list and update apt again:

```echo "deb [ arch=arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list```

```sudo apt-get update```

Finally we can install mongodb:

```sudo apt-get install mongodb-org```


Step 4 - amend config.txt to allow the CANbus to be recognised

Edit ```/boot/config.sys``` by adding the following lines at the end of the file:

```dtparam=spi=on```

```dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25```

```dtoverlay=spi-bcm2835-overlay```

(Note that ```dtparam=spi=on``` can be set through ```raspi-config``` or simply uncommented earlier in the ```config.txt``` file)

It is important to check the bitrate in these lines - the PiCAN2 uses the MCP2515	CAN	controller which needs an oscillator setting of 16000000. We did set the oscillator to 8000000 in previous attempts, reading from the wrong datasheet, which caused issues with the whole vehicle's bus...


#### Python packages

We now need to install some dependencies in pip so that we can access the CANbus and through python.

There are three that we need: ```pymongo```, which allows us to access the mongodb with python; ```python-can``` which connects us to the CANbus; and ```opencv-python``` which will allow us to run opencv, which will handle our display in an extensible fashion.

```pip3 install pymongo```

```pip3 install python-can```

```pip3 install opencv-python```

#### Preparing the system *****Very much incomplete at this stage*****

Bring up the CANbus:

In order to register the CANbus as a network like any other in linux, accessible through Berkeley sockets (thanks Volkswagen!), we need to bring up the CAN network as follows:

```sudo /sbin/ip link set can0 up type can bitrate 500000```
