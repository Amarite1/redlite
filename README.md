# redlite
Goal light software for NHL games. Redlite pulls publicly available play-by-play data from the NHL website to determine when a goal has been scored. Included in this repository are a few different example applications (explained below) that can be used in conjunction with DIY hardware devices. In addition, the core Python script can be used to create custom implemenations.

Redlite is not affiliated with, or endorsed by, the National Hockey League (NHL) or any other entity.

## Files
- core.py : The core code that makes the web requests - acts like a module/library
- test.py : Test client that outputs goal event to the console
- desktop.py : [Untested] Desktop client that sends goal events over serial to a connected controller (eg. Arduino)
- onion.py : [Partially Tested] Client for the Onion Omega that turns on a GPIO pin when there's a goal
- rpi.py : Client for the Raspberry Pi that turns on a GPIO pin when there's a goal

## Setup
Find your platform below for instructions on installation and configuration of redlite.

### Raspberry Pi
*Coming Soon*

### Onion Omega
Starting from a fresh Omega, you will need to install a few packages using `opkg install <package>` via the terminal

Required Packages:
- python3-light
- python3-email
- python3-codecs

Optional packages that may make your life easier:
- git
- git-http

If you installed `git` and `git-http`, you can clone the code you need directly from the URLs below. Otherwise, you will need to download them yourself and transfer them to your Omega.
- redlite: https://github.com/Amarite1/redlite
- OmegaGPIO: https://github.com/BravoPapa/OmegaGPIO

To save space, you can delete all the files from redlite EXCEPT `core.py` and `onion.py`. You will need to copy `omega_gpio.py` from the OmegaGPIO directory into the redlite directory. The other OmegaGPIO files can be deleted to save space as well.

Finally, you need to configure the script to match your configuration. To do this, open `onion.py` in a text editor on the Omega (eg. `vi`) and change `GPIO_PIN` to be whichever pin you want to use on your Omega. You can also change `LIGHT_ON_SECONDS` to define how long (in seconds) you want the goal light to stay on.

## Running
Once you've setup your redlite script, you can run it using `python3 <file>`. For example, `python3 onion.py` will run the Onion Omega version of redlite. You will need to enter your desired team's three-character code. To see all the codes, enter `LIST` at this point and find the code that corresponds to your team. redlite is now polling for goals and will turn on a GPIO/send a serial message/show a console message when your team scores a goal!