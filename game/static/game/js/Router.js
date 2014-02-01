$(function(){
	var Router = Backbone.Router.extend({
		routes: {
			"game/:id": "game",
			"about": "about",
			"lobby": "lobby",
			"": "lobby"
		},

		game: function(id){
			cardsAgainstHumanity.vent.trigger("showGame", id);
		},

		about: function(){
			cardsAgainstHumanity.vent.trigger("showAbout");
		},

		lobby: function(){
			cardsAgainstHumanity.vent.trigger("showLobby");
		}
	});
	new Router();
});
