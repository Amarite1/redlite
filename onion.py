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
import omega_gpio
from sys import exit
import time

# Configuration Constants
GPIO_PIN = 1
LIGHT_ON_SECONDS = 20 # how long to keep the light on as a multiple of REFRESH_RATE (eg. 1 means 1 x REFRESH_RATE)

# Global Vars
cyclesOn = 0
lightOn = False
refreshCounter = 0

# Setup
omega_gpio.initpin(GPIO_PIN,'out')
team = redlite.promptTeam()

if(team == ""):
	print("Exiting...")
	omega_gpio.closepin(GPIO_PIN,'out')
	exit()

game, teamType = rl.findGame(t)

if game == -1:
	print("No Game Today")
	omega_gpio.closepin(GPIO_PIN,'out')
	exit()

data = rl.loadGameData(game, teamType)

refreshRate = data[0]
team = data[1]
lastEvent = data[2]

# Main Loop
while(True):
	
	if (lightOn == True):
		cyclesOn = cyclesOn + 1

	if (cyclesOn >= LIGHT_ON_SECONDS):
		omega_gpio.setoutput(GPIO_PIN, 0)
		cyclesOn = 0
		lightOn = False

	if(refreshCounter >= refreshRate):

		refreshCounter = 0

		goal, lastEvent, refreshRate = rl.goal(game, team, lastEvent)

		if (goal):
			omega_gpio.setoutput(GPIO_PIN, 1)
			lightOn = True

	else:
		refreshCounter = refreshCounter + 1

	if(refreshRate == 0):
		break

	time.sleep(1)

# End of Main Loop

# Shutdown
omega_gpio.closepin(GPIO_PIN,'out')