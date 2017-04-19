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
import serial
from sys import exit

# Constants
SERIAL_PORT = "COM1"
LIGHT_ON_SECONDS = 20
COMMAND_ON = "on"
COMMAND_OFF = "off"

# Global Variables
cyclesOn = 0
lightOn = False
refreshCounter = 0

# Setup
team = redlite.promptTeam()

if(team == ""):
	print("Exiting...")
	exit()

game, teamType = redlite.findGame(t)

if game == -1:
	print("No Game Today")
	exit()

data = redlite.loadGameData(game, teamType)

refreshRate = data[0]
team = data[1]
lastEvent = data[2]

ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# Main Loop
while(True):
	
	if (lightOn == True):
		cyclesOn = cyclesOn + 1

	if (cyclesOn >= LIGHT_ON_SECONDS):
		ser.write(COMMAND_OFF)
		cyclesOn = 0
		lightOn = False

	if(refreshCounter >= refreshRate):

		refreshCounter = 0

		goal, lastEvent, refreshRate = redlite.goal(game, team, lastEvent)

		if (goal):
			ser.write(COMMAND_ON)
			lightOn = True

	else:
		refreshCounter = refreshCounter + 1

	if(refreshRate == 0):
		break

	time.sleep(1)

# End of Main Loop
