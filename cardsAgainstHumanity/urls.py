from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from game import views

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'cardsAgainstHumanity.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^game/(?P<game_id>\d+)/gamePlayer/(?P<gameplayer_id>\d+)', views.gamePlayer),
	url(r'^game/(?P<game_id>\d+)/gameRound/(?P<gameround_id>\d+)', views.gameRound),
	url(r'^game/(?P<game_id>\d+)/addPlayer/(?P<playerhash>\w+)', views.addPlayer),
	url(r'^game/(?P<game_id>\d+)', views.game),
	url(r'^setPlayerName/(?P<name>\w+)', views.setPlayerName),
	url(r'^newGame', views.newGame),
	url(r'^lobby', views.lobby),
	url(r'^.*$', views.index),
)
