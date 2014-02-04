from django.shortcuts import render
from django.http import HttpResponse

from game.models import Player, Game

import random, json

def index(request):
	playerhash = "%032x" % random.getrandbits(128)
	name = ""
	if request.COOKIES.has_key("playerhash"):
		playerhash = request.COOKIES["playerhash"]
		player, created = Player.objects.get_or_create(hash = playerhash)
		name = player.name
	return render(request, 'game/index.html', {'playerhash': playerhash, 'playername': name})

def setPlayerName(request, name):
	playerhash = request.COOKIES["playerhash"]
	player = Player.objects.get(hash = playerhash)
	player.name = name
	player.save()
	return HttpResponse(status = 200)

def lobby(request):
	responseData = []
	for game in Game.objects.filter(active = 0).order_by("-gameplayer__datetimeCreated","-id")[:100]:
		responseData.append({
			"id": game.id,
			"numberOfPlayers": game.getNumberOfPlayers(),
			"secondsSinceLastPlayerJoined": game.getSecondsSinceLastPlayerJoined(),
		})
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def newGame(request):
	game = Game.objects.create()

	responseData = { "id": game.id, }
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def addBot(request, game_id):
	game = Game.objects.get(id = game_id).addPlayer()
	return HttpResponse(status = 200)

def startGame(request, game_id):
	Game.objects.get(id = game_id).startGame()
	return HttpResponse(status = 200)

def game(request, game_id):
	game = Game.objects.get(id = game_id)

	player = Player.objects.get(hash = request.COOKIES["playerhash"])
	game.addPlayer(player)

	return HttpResponse(json.dumps(getGameJSON(game)), content_type="application/json")

def getGameJSON(game):
	return {
		"id": game.id,
		"active": game.active,
		"gamePlayers": [
			{
				"id": gamePlayer.id,
				"hash": gamePlayer.getHash(),
				"name": gamePlayer.getName(),
				"gameCards": [
					{
						"card_id": gameCard.card.id,
						"text": gameCard.card.text
					} for gameCard in game.gamecard_set.filter(game = game, gamePlayer = gamePlayer).order_by("id")
				],
			} for gamePlayer in game.gameplayer_set.filter(game = game).order_by("id")
		],
		"gameRounds": [
			{
				"id": gameRound.id,
				"gamePlayerQuestioner_id": gameRound.gamePlayerQuestioner_id,
				"question": gameRound.gameCardQuestion.card.text,
				"answers": [
					{
						"text": answer.gameCard.card.text,
						"gameplayer_id": answer.gamePlayer.id,
						"card_id": answer.gameCard.card.id,
						"winner": answer.winner,
					} for answer in gameRound.gameroundanswer_set.all()
				],
			} for gameRound in game.gameround_set.filter(game = game).order_by("id")
		],
	}

def submitAnswer(request, game_id, card_id):
	player = Player.objects.get(hash = request.COOKIES["playerhash"])
	game = Game.objects.get(id = game_id)
	gamePlayer = game.gameplayer_set.get(game = game, player = player)
	gameCard = game.gamecard_set.get(game = game, gamePlayer = gamePlayer, card_id = card_id)
	game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard)
	return HttpResponse(status = 200)

def chooseWinner(request, game_id, card_id):
	game = Game.objects.get(id = game_id)
	gameRound = game.gameround_set.filter(game = game).order_by("-id").first()
	gameCard = game.gamecard_set.get(game = game, card_id = card_id)
	gameRoundAnswer = gameRound.gameroundanswer_set.get(gameRound = gameRound, gameCard = gameCard)

	gameRoundAnswer.winner = 1
	gameRoundAnswer.save()

	return HttpResponse(status = 200)

def forceAnswers(request, game_id):
	game = Game.objects.get(id = game_id)

	for gamePlayer in game.gameplayer_set.all():
		randomGameCard = gamePlayer.gamecard_set.filter(gamePlayer = gamePlayer).order_by("?").first()
		game.gamePlayerSubmitsAnswerCard(gamePlayer, randomGameCard)

	return HttpResponse(status = 200)

def gameRound(request, game_id, gameround_id):
	game = Game.objects.get(id = game_id)
	gameRound = game.gameround_set.filter(game = game)
	responseData = {
		"id": gameRound.id,
		"question": gameRound.gameCardQuestion.card.text,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")
