from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from game import views

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'cardsAgainstHumanity.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^game/(?P<game_id>\d+)/gameRound/(?P<gameround_id>\d+)', views.gameRound),
	url(r'^game/(?P<game_id>\d+)/submitAnswer/(?P<card_id>\d+)', views.submitAnswer),
	url(r'^game/(?P<game_id>\d+)/chooseWinner/(?P<card_id>\d+)', views.chooseWinner),
	url(r'^game/(?P<game_id>\d+)/forceAnswers', views.forceAnswers),
	url(r'^game/(?P<game_id>\d+)/addBot', views.addBot),
	url(r'^game/(?P<game_id>\d+)/start', views.startGame),
	url(r'^game/(?P<game_id>\d+)', views.game),
	url(r'^setPlayerName/(?P<name>\w+)', views.setPlayerName),
	url(r'^newGame', views.newGame),
	url(r'^lobby', views.lobby),
	url(r'^.*$', views.index),
)
