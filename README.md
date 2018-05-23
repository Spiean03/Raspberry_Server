# Raspberry_Server
DataLogger. Data is stored on a Raspberry Pi Server; Bokeh interactive visualization library is used to update the plot.

![alt text](/crossfilter/Screenshot_1.jpg )

Set a fixed ip:
````
$ sudo nano  /etc/network/interfaces

auto eth0
iface eth0 inet static
    address 192.168.1.42
    netmask 255.255.255.0
    gateway 192.168.1.1
````

Install following packages/ do the following in the terminal:
````
$ sudo apt-get install pigpio python-pigpio

$ sudo apt-get install git

$ sudo apt-get install build-essential python-dev
````

Get the Adafruit DHT11 Package:
````
$ git clone https://github.com/adafruit/Adafruit_Python_DHT 
````
If not available, use copy from my github:
````
$ git clone https://github.com/Spiean03/Adafruit_Python_DHT
````

go to the folder ($ cd Adafruit_Python_DHT) where the DHT_setup.py file is and install it:
````
$ sudo python setup.py install
````

if the sensor is correctly installed, you can go to the examples files 

(the number '11' stands for the sensor you are using, either DHT11, DHT22, 2302) and '4' for the pigpio pin):
````
$ cd examples

$ sudo ./AdafruitDHT.py 11 4
````

install Apache:
````
$ sudo apt-get install apache2 -y
````

install PHP:
````
$ sudo apt-get install php libapache2-mod-php -y
````
This default web page is just a HTML file on the filesystem. It is located at /var/www/html/index.html, so go there:
````
$ cd /var/www/html/

$ ls -al
````
To access the website, find your IP of your Raspberry first:
````
$ hostname -I
````
If you now enter the IP of your Raspberry in your browser, you will be directed to the html page



Now get Bokeh:

````
$ sudo apt-get install python-pandas

$ sudo pip install ipython

$ pip --no-cache-dir install bokeh

$ sudo pip install numexpr --upgrade

$ pip install numpy –upgrade
````
Start script automatically on bootup:
````
$ sudo nano /etc/rc.local 

add the following line to the script, where scriptname.py should be /home/pi/Raspberry_Server/Run_main.py:
(sleep 1;python scriptname.py)&
````
When you have installed bokeh on your computer, place the folder 'crossfilter' into the bokeh directory (c:/users/user/..). In the CMD, type:
````
bokeh serve --show crossfilter
````
This will run the application.
