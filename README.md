# redlite
Goal light software for NHL games. Redlite pulls publicly available play-by-play data from the NHL website to determine when a goal has been scored. Included in this repository are a few different example applications (explained below) that can be used in conjunction with DIY hardware devices. In addition, the core Python script can be used to create custom implemenations.

Redlite is not affiliated with, or endorsed by, the National Hockey League (NHL) or any other entity.

## Files
- core.py : The core code that makes the web requests - acts like a module/library
- test.py : Test client that outputs goal event to the console
- desktop.py : [Untested] Desktop client that sends goal events over serial to a connected controller (eg. Arduino)
- onion.py : [Untested] Client for the Onion Omega that turns on a GPIO pin when there's a goal
- rpi.py : Client for the Raspberry Pi that turns on a GPIO pin when there's a goal
