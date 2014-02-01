from django.shortcuts import render
from django.http import HttpResponse

from game.models import Player, Game

import random, json

def index(request):
	if request.COOKIES.has_key("playerhash"):
		playerhash = request.COOKIES["playerhash"]
	else:
		playerhash = "%032x" % random.getrandbits(128)
	return render(request, 'game/index.html', {'playerhash': playerhash})

def setPlayerName(request):
	playerhash = request.POST.get("playerhash", "")
	name = request.POST.get("name", "")

	player = Player.models.get_or_create(hash = playerhash)
	player.name = name
	player.save()
	return HttpResponse(status = 200)

def lobby(request):
	responseData = []
	for game in Game.objects.filter(active = 0).order_by("-gameplayer__datetimeCreated")[:100]:
		responseData.append({
			"id": game.id,
			"numberOfPlayers": game.getNumberOfPlayers(),
			"secondsSinceLastPlayerJoined": game.getSecondsSinceLastPlayerJoined(),
		})
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def newGame(request):
	game = Game.objects.create()
	responseData = {
		"id": game.id,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def addPlayer(request, game_id, playerhash):
	game = Game.objects.get(id = game_id)
	if Player.objects.filter(hash = playerhash).exists():
		player = Player.objects.get(hash = playerhash)
	else:
		player = None
	game.gameplayer_set.create(game = game, player = player)
	return HttpResponse(status = 200)

def game(request, game_id):
	game = Game.objects.get(id = game_id)
	responseData = {
		"id": game.id,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def gamePlayer(request, game_id, gameplayer_id):
	return HttpResponse("this is the gamePlayer view")

def gameRound(request, game_id, gameround_id):
	return HttpResponse("this is the gameRound view")
