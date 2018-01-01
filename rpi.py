'''
 ' This file is part of redlite.
 '
 ' redlite is free software: you can redistribute it and/or modify
 ' it under the terms of the GNU General Public License as published by
 ' the Free Software Foundation, either version 3 of the License, or
 ' (at your option) any later version.
 '
 ' redlite is distributed in the hope that it will be useful,
 ' but WITHOUT ANY WARRANTY; without even the implied warranty of
 ' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 ' GNU General Public License for more details.
 '
 ' You should have received a copy of the GNU General Public License
 ' along with redlite.  If not, see <http://www.gnu.org/licenses/>.
'''

import core as redlite
import RPi.GPIO as gpio
from sys import exit
import time

# Configuration Constants
GPIO_PIN = 4
GPIO_MODE = gpio.BCM
LIGHT_ON_SECONDS = 20

# Global Vars
cyclesOn = 0
lightOn = False
refreshCounter = 0

# Setup
gpio.setmode(GPIO_MODE)
gpio.setup(GPIO_PIN, gpio.OUT, initial=gpio.HIGH)
gpio.setup(17, gpio.OUT, initial=gpio.HIGH)
gpio.setup(27, gpio.OUT, initial=gpio.HIGH)
team = redlite.promptTeam()

print("WARNING: This script is out of date and WILL NOT WORK with the new version of redlite!")
exit()

if(team == ""):
	print("Exiting...")
	gpio.cleanup()
	exit()

game, teamType = redlite.findGame(team)

if game == -1:
	print("No Game Today")
	gpio.cleanup()
	exit()

data = redlite.loadGameData(game, teamType)

refreshRate = data[0]
team = data[1]
lastEvent = data[2]

# Main Loop
while(True):
	
	if (lightOn == True):
		cyclesOn = cyclesOn + 1

	if (cyclesOn >= LIGHT_ON_SECONDS):
		gpio.output(GPIO_PIN, gpio.HIGH)
		cyclesOn = 0
		lightOn = False

	if(refreshCounter >= refreshRate):

		refreshCounter = 0

		goal, lastEvent, refreshRate = redlite.goal(game, team, lastEvent)

		if (goal):
			gpio.output(GPIO_PIN, gpio.LOW)
			lightOn = True

	else:
		refreshCounter = refreshCounter + 1

	if(refreshRate == 0):
		break

	time.sleep(1)

# End of Main Loop

# Shutdown
gpio.cleanup()