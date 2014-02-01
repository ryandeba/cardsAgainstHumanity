$(function(){
	var Router = Backbone.Router.extend({
		initialize: function(){
			this.listenTo(cardsAgainstHumanity.vent, "navigate", this.navigateTo);
		},

		routes: {
			"game/:id": "game",
			"about": "about",
			"lobby": "lobby",
			"": "lobby"
		},

		navigateTo: function(url){
			this.navigate(url, {trigger: true});
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
