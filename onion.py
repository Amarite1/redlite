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
import time

# Configuration Constants
GPIO_PIN = 1
REFRESH_RATE = 20
LIGHT_ON_CYCLES = 1 # how long to keep the light on as a multiple of REFRESH_RATE (eg. 1 means 1 x REFRESH_RATE)

# Global Vars
cyclesOn = 0

# Setup
omega_gpio.initpin(GPIO_PIN,'out')
team = redlite.promptTeam()

if(team == ""):
	print("Exiting...")
	omega_gpio.closepin(GPIO_PIN,'out')
	return

# Main Loop
while(True):
	
	if (cyclesOn > 0):
		cyclesOn ++

	if (cyclesOn > LIGHT_ON_CYCLES):
		omega_gpio.setoutput(GPIO_PIN, 0)
		cyclesOn = 0

	if (redlite.goal()):
		omega_gpio.setoutput(GPIO_PIN, 1)
		cyclesOn = 1

	time.sleep(REFRESH_RATE)

# End of Main Loop

# Shutdown
omega_gpio.closepin(GPIO_PIN,'out')