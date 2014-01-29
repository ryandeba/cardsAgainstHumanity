from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from game import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cardsAgainstHumanity.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', views.login, name = "login"),
    url(r'^register', views.register, name = "register"),
    url(r'^lobby', views.lobby, name = "lobby"),
    url(r'^game/(?P<game_id>\d+)', views.game, name = "game"),
    url(r'^.*$', views.index, name = "index"),
)
