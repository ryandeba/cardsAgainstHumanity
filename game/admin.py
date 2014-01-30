from django.contrib import admin
from game.models import Card, Player, Game, GamePlayer, GameCard

admin.site.register(Card)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(GameCard)
