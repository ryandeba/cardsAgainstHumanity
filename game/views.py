from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

def index(request):
	return render(request, 'game/index.html')

def login(request):
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	user = authenticate(username = username, password = password)
	if user is not None:
		auth_login(request, user)
		return HttpResponse(status = 200)
	else:
		return HttpResponse(status = 401)

def register(request):
	username = request.POST.get("username", "")

	existingUsersWithUsername = User.objects.filter(username = username)
	if len(existingUsersWithUsername) > 0:
		return HttpResponse(status = 409)

	password = request.POST.get("password", "")
	user = User.objects.create_user(username, username + "@email.com", password)
	user.save()
	user = authenticate(username = username, password = password)
	auth_login(request, user)
	return HttpResponse(status = 200)

def lobby(request):
	return HttpResponse("this is the lobby")

def game(request, game_id):
	return HttpResponse("this is the game for id %s" % game_id)
