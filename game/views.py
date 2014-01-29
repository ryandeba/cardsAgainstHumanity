from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
	return render(request, 'game/index.html')

def login(request):
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	user = authenticate(username = username, password = password)
	if user is not None:
		return HttpResponse(status = 200)
	else:
		return HttpResponse(status = 401)

def register(request):
	return HttpResponse("this is the register endpoint")

def lobby(request):
	return HttpResponse("this is the lobby")

def game(request, game_id):
	return HttpResponse("this is the game for id %s" % game_id)
