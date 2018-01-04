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
import encodings.idna
import omega_gpio
from sys import exit
import time

# Configuration Constants
GPIO_PINS_R = [1, 6 ,7, 8]
GPIO_PINS_G = [18, 19, 20, 21]
GPIO_PINS = GPIO_PINS_R + GPIO_PINS_G
LIGHT_ON_SECONDS = 20

# Global Vars
cyclesOn = 0
lightOn = False
refreshCounter = 0

# Light Functions
def initLight():
	for pin in GPIO_PINS:
		omega_gpio.initpin(pin, 'out')

def testLight():
	setLight(0)
	time.sleep(0.5)
	setLight(1)
	time.sleep(0.5)
	setLight(2)
	time.sleep(0.5)
	setLight(0)

def endLight():
	for pin in GPIO_PINS:
		omega_gpio.closepin(pin)

def setLight(state):
	if state == 0:
		for pin in GPIO_PINS:
			omega_gpio.setoutput(pin, 0)

	elif state == 1:
		for pin in GPIO_PINS_R:
			omega_gpio.setoutput(pin, 1)

	elif state == 2:
		for pin in GPIO_PINS_G:
			omega_gpio.setoutput(pin, 1)

# Setup
try:
	initLight()
except:
	endLight()
	initLight()

testLight()
setLight(2)

team = redlite.promptTeam()

if(team == ""):
	print("Exiting...")
	endLight()
	exit()

game, teamType = redlite.findGame(team)

if game == -1:
	print("No Game Today")
	endLight()
	exit()

data = redlite.loadGameData(game, teamType)

refreshRate = data[0]
lastScore = data[1]

# Main Loop
while(True):
	
	if (lightOn == True):
		cyclesOn = cyclesOn + 1

	if (cyclesOn >= LIGHT_ON_SECONDS):
		setLight(0)
		cyclesOn = 0
		lightOn = False

	if(refreshCounter >= refreshRate):

		refreshCounter = 0

		goal, lastScore, refreshRate = redlite.goal(game, teamType, lastScore)

		if (goal):
			setLight(1)
			lightOn = True

	else:
		refreshCounter = refreshCounter + 1

	if(refreshRate == 0):
		break

	time.sleep(1)

# End of Main Loop

# Shutdown
omega_gpio.closepin(GPIO_PIN)