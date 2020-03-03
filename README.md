# PI-ENVIRO


## Project Info
Project | Pi-Enviro       
------- | ---------
Board | RPi 3	        
Temp-Humid Sensor | DHT-22        	
OLED Display | SH1106        	
Python Version | 3.7.3           

## Install Libraries

### MatPlotLib
	1. Run the following commands to install matplotlib for python (refer to notes on python version)
		python3 -m pip install -U pip
		python3 -m pip install -U matplotlib

### Adafruit Library
	1. Install some essential packages
		sudo apt-get install build-essential python-dev python-openssl git

	2. Clone the Adafruit library and setup the python library
		git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
		sudo python3 setup.py install

		![alt-text](https://github.com/george-howell/pi-enviro/blob/readme-update/docs/sh1106/ssd1331-oled-display-raspberry-pi-connection.jpg)

### OLED Library
Instructions taken from here: [Luma OLED Library](https://luma-oled.readthedocs.io/en/latest/intro.html)
	
	1. Install the latest version of the library
		sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 libtiff5
		sudo -H pip3 install --upgrade luma.oled

### Notes
	1. The use of python or python3 depends on which version of python it linked. This can be checked with 'python{x} --version'. As standard, the Raspberry Pi will link 'python' to Python 2.7.3, and 'python3' to Python 3+.

## Start Program
	1. Navigate to the folder containing the code
	2. Start the program using the following
		python3 {progName}.py --display sh1106 --interface spi
	3. Or, type
		/.run



