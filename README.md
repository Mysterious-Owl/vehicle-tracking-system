# Vehicle Tracking System

Vehicle Tracking System is a system which will track the live position of vehicle with the help of satellites. Here we tried to reproduce the same, with all the software and the hardware support. In general, tracking of vehicles is a process in which we request the location in form of latitude and longitude (Geographic Coordinates) and send them to the server. Geographic Coordinates can pin point any location on Earth. This system is very efficient for outdoor application purposes, having accuracy of about 5m. These devices are widely used in tracking passenger vehicles, stolen vehicles, school/college buses, etc. They are very commonly used in fleet management and asset tracking applications. Today these systems can not only track the location of the vehicle but can also report the speed and locate the vehicle on the map. They can be used for multiple vehicles simultaneously and can be used from anywhere in world with the help of internet.

## Includes -
 - Vehicle Device(hardware): 
    - GPS module
    - ATmega328p
    - GSM module
- Server(software):
    - Flask (PYTHON)
    - HTML
    - Google Maps API
    - JavaScript
    - CSS

## Features - 
- Shows last location of user
- Can have multiple  users
- Path tracing for all users
- Different color for path for different users

## How to use - 
### For Hardware Simulation
- Generate HEX file of [Microcontroller code](/Code/Microcontroller/gps.ino) by Arduino IDE
- Upload this code in microcontroller in [Proteus file](/Code/Microcontroller/GPS.pdsprj)
- Reply the AT commands with their expected outcome, see GSM dump(page 26) of [Report](/Report.pdf)

### For Software Simulation
- Download the files
- Open [batch file](/Code/server/run.bat) or run [Python file](/Code/server/main.py)
- Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Images -

### Schematic Capture
![SCHEMATIC](/Images/Schematic.png)

### Simulation
![Simulation](/Images/Simulation.png)

### Webpage
![Webpage](/Images/Webpage.png)
