from django.shortcuts import render
from django.http import HttpResponse

from game.models import Player, Game

import random

def index(request):
	playerhash = "%032x" % random.getrandbits(128)
	return render(request, 'game/index.html', {'playerhash': playerhash})

def setPlayerName(request):
	playerhash = request.POST.get("playerhash", "")
	name = request.POST.get("name", "")

	players = Player.models.filter(hash = playerhash)
	if len(players) == 0:
		player = Player(hash = playerhash)
	else:
		player = players[0]
	player.name = name
	player.save()
	return HttpResponse(status = 200)

def lobby(request):
	return HttpResponse("this is the lobby")

def newGame(request):
	game = Game()

def game(request, game_id):
	return HttpResponse("this is the game for id %s" % game_id)
