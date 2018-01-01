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

import json
import subprocess
import time
from socket import error as SocketError
from urllib.request import urlopen


#CONSTANTS
URL_SCHED_PROTO = "http://live.nhl.com/GameData/SeasonSchedule-{season}.json"
URL_GAME_PROTO = "http://statsapi.web.nhl.com/api/v1/game/{game}/feed/live"

TEAM_CODES = [
				"TOR", "OTT", "CGY", "EDM", "STL",
				"CHI", "LAK", "SJS", "MTL", "BUF",
				"NYI", "NYR", "WSH", "PIT", "CBJ",
				"DET", "TBL", "NJD", "FLA", "MIN",
				"CAR", "WPG", "ANA", "DAL", "PHI",
				"VAN", "ARI", "BOS", "NSH", "COL"
			];

def promptTeam():
	print("Enter your team's 3-character code: ")
	team = input("> ")

	if team in TEAM_CODES:
		return team
	elif team == "LIST":
		print(TEAM_CODES)
		return promptTeam()
	elif team == "EXIT":
		return ""
	else:
		print("Invalid Team! Try again or type 'LIST' or 'EXIT'")
		return promptTeam()
# end of promptTeam

def getSeasonId():
	curTime = time.localtime()
	if (curTime.tm_mon <= 7):
		return "{0}{1}".format(curTime.tm_year-1, curTime.tm_year)
	else:
		return "{0}{1}".format(curTime.tm_year, curTime.tm_year+1)
	
# end getSeasonId

def findGame(team):
	schedResp = __loadUrl(URL_SCHED_PROTO.format(season=getSeasonId()))
	games = json.loads(schedResp)

	dateStr = time.strftime("%Y%m%d", time.localtime())
	gameId = -1 # game ID to use
	teamType = -1 # whether the team is home (0) or away (1)
	for game in games:
		
		if game["est"].startswith(dateStr):

			if game["a"] == team.upper():
				teamType = "away"
				gameId = game["id"]
				break
			elif game["h"] == team.upper():
				teamType = "home"
				gameId = game["id"]
				break

	return [gameId, teamType]
# end of findGame

def loadGameData(gameId, teamType):
	gameResp = __loadUrl(URL_GAME_PROTO.format(game=gameId))

	data = json.loads(gameResp)

	return [data["metaData"]["wait"], data["liveData"]["boxscore"]["teams"][teamType]["teamStats"]["teamSkaterStats"]["goals"]]
# end of loadGameData

def goal(gameId, teamType, lastScore):
	try:
		gameResp = __loadUrl(URL_GAME_PROTO.format(game=gameId))

		data = json.loads(gameResp)
		goal = False

		score = data["liveData"]["boxscore"]["teams"][teamType]["teamStats"]["teamSkaterStats"]["goals"]
		if(lastScore < score):
			goal = True

	except (ValueError, SocketError) as e:
		print(e)
		time.sleep(1)
		return [False, lastScore, 5]

	return [goal, score, data["metaData"]["wait"]]
# end of goal

def __loadUrl(url):
	return urlopen(url).read().decode("UTF-8")