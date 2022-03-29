# Environment_Logger
Code for arch linux temperature and humidity loggers

This code creates a database, then reads the DHT22 to take in temperature and humidity data.
The data is then stored in the database for one hour, upon which it will be uploaded and deleted.

Currently the code is being run using a Raspberry Pi Zero running Arch Linux with a DHT22 and Microswitch.


Problem Statement: An opportunity has been found to improve the management of the chilled storage in the ----- site in ---------. The system should meet the following criteria:

Initial Requirements:
1.	Measure the temperature of the temperature controlled storage 
2.	Record daily results and upload to secure storage
3.	Provide an alert should a temperature threshold be breached
4.	Ability to access current and historic temperature reading remotely
5.	The device should locally display the ambient temperature and target temperature
6.	The device should locally display IP address
7.	The device should locally display any alarm conditions
8.	The unit should have a minimum of 12 hours of battery backup should power be lost.
9.	The unit should report and record the duration of any power looses
10.	Provide user and operating instructions and team training
11.	The unit should be able to accept calibration offset
12. The unit should detect if the door is securly closed
13. The unit should have an audiable signal should rules of temperature or door open time are breached.
