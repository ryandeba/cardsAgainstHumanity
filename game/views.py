from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateformat import format
from django.utils.timezone import utc
from django.db.models import Q

from game.models import Player, Game

import random, json, time, datetime

def index(request):
	playerhash = "%032x" % random.getrandbits(128)
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
	playerhash = request.COOKIES["playerhash"]
	player = Player.objects.get(hash = playerhash)
	responseData = []
	for game in Game.objects.filter(active = 0).order_by("-gameplayer__datetimeCreated","-id")[:50]:
		responseData.append({
			"id": game.id,
			"numberOfPlayers": game.getNumberOfPlayers(),
			"secondsSinceLastPlayerJoined": game.getSecondsSinceLastPlayerJoined(),
		})
	for game in Game.objects.filter(active = 1, gameplayer__player_id = player.id):
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
	game.applyAllAvailableGameActions()
	gamePlayer = game.gameplayer_set.all().filter(player = player).first()

	responseData = getGameJSON(
		game = game,
		thisPlayer = gamePlayer,
		datetimeLastUpdated = timestampToDatetime(request.GET.get("lastUpdated", "0"))
	)
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def submitAnswer(request, game_id, card_id):
	player = Player.objects.get(hash = request.COOKIES["playerhash"])
	game = Game.objects.get(id = game_id)
	gamePlayer = game.gameplayer_set.get(game = game, player = player)
	gameCard = game.gamecard_set.get(game = game, gamePlayer = gamePlayer, card_id = card_id)
	game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard)
	return HttpResponse(status = 200)

def chooseWinner(request, game_id, card_id):
	game = Game.objects.get(id = game_id)
	player = Player.objects.get(hash = request.COOKIES["playerhash"])
	gameCard = game.gamecard_set.get(game = game, card_id = card_id)
	gamePlayer = game.gameplayer_set.get(game = game, player = player)
	game.gamePlayerPicksWinningAnswerCard(gamePlayer, gameCard)
	return HttpResponse(status = 200)

def getGameJSON(game, thisPlayer, datetimeLastUpdated):
	result = {
		"lastUpdated": datetimeToEpoch(datetime.datetime.utcnow()),
		"id": game.id,
		"active": game.active,
		"thisPlayersAnswerCards": [
			{
				"card_id": gameCard.card.id,
				"text": gameCard.card.text
			} for gameCard in game.gamecard_set.filter(game = game, gamePlayer = thisPlayer, datetimeLastModified__gte = datetimeLastUpdated).exclude(gamePlayer_id = None)
		],
		"gamePlayers": [
			{
				"id": gamePlayer.id,
				"hash": gamePlayer.getHash(),
				"name": gamePlayer.getName(),
				"points": gamePlayer.getPoints(),
			} for gamePlayer in game.gameplayer_set.all().filter(Q(datetimeLastModified__gte = datetimeLastUpdated) | Q(player__datetimeLastModified__gte = datetimeLastUpdated)).order_by("id")
		],
		"gameRounds": [
			{
				"id": gameRound.id,
				"gamePlayerQuestioner_id": gameRound.gamePlayerQuestioner_id,
				"question": gameRound.gameCardQuestion.card.text,
				"isComplete": gameRound.isComplete(),
				"answers": [
					{
						"text": answer.gameCard.card.text,
						"gameplayer_id": answer.gamePlayer.id,
						"card_id": answer.gameCard.card.id,
						"winner": answer.winner,
					} for answer in gameRound.gameroundanswer_set.all()
				],
			} for gameRound in game.gameround_set.all().filter(datetimeLastModified__gte = datetimeLastUpdated).order_by("id")
		],
	}
	if len(result['gameRounds']) == 0:
		del result['gameRounds']
	if len(result['gamePlayers']) == 0:
		del result['gamePlayers']
	if len(result['thisPlayersAnswerCards']) == 0:
		del result['thisPlayersAnswerCards']
	return result

def datetimeToEpoch(datetime):
	return str(time.mktime(datetime.timetuple()) + float("0.%s" % datetime.microsecond))

def timestampToDatetime(timestamp):
	return datetime.datetime.utcfromtimestamp(float(timestamp)).replace(tzinfo = utc)
