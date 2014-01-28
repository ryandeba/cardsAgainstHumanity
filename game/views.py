from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'game/index.html')

def lobby(request):
	return HttpResponse("this is the lobby")

def game(request, game_id):
	return HttpResponse("this is the game for id %s" % game_id)
