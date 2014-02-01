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
		game.gameplayer_set.get_or_create(game = game, player = player)
	else:
		game.gameplayer_set.create(game = game)
	return HttpResponse(status = 200)

def game(request, game_id):
	game = Game.objects.get(id = game_id)
	responseData = {
		"id": game.id,
		"active": game.active,
		"gamePlayers": [{"id": gamePlayer.id} for gamePlayer in game.gameplayer_set.filter(game = game).order_by("id")],
		"gameRounds": [{"id": gameRound.id} for gameRound in game.gameround_set.filter(game = game).order_by("id")],
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def gamePlayer(request, game_id, gameplayer_id):
	game = Game.objects.get(id = game_id)
	gamePlayer = game.gameplayer_set.get(id = gameplayer_id)
	name = ""
	if gamePlayer.player:
		name = gamePlayer.player.name
	responseData = {
		"id": gamePlayer.id,
		"name": name,
		"gameCards": [
			{"id": gameCard.id, "text": gameCard.card.text}
			for gameCard in game.gamecard_set.filter(game = game, gamePlayer = gamePlayer).order_by("id")
		],
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def gameRound(request, game_id, gameround_id):
	game = Game.objects.get(id = game_id)
	gameRound = game.gameround_set.filter(game = game)
	responseData = {
		"id": gameRound.id,
		"question": gameRound.gameCardQuestion.card.text,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")
