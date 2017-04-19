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

import core as rl
from sys import exit
import time

t = rl.promptTeam()
game, teamType = rl.findGame(t)

if (game == -1):
	print("No Game Today!")
	exit()


data = rl.loadGameData(game, teamType)

interval = data[0]
team = data[1]
lastEvent = data[2]

while(True):

	goal, lastEvent, interval = rl.goal(game, team, lastEvent)

	if(goal):
		print("%s GOAL!"%t)

	if(interval == 0):
		print("Game Over")
		exit()

	time.sleep(interval)
# end while