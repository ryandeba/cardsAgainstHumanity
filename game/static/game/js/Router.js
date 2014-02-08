$(function(){
	var Router = Backbone.Router.extend({
		initialize: function(){
			this.listenTo(cardsAgainstHumanity.vent, "navigate", this.navigateTo);
		},

		routes: {
			"game/:id": "game",
			"about": "about",
			"lobby": "lobby",
			"newgame": "newgame",
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
		},

		newgame: function(){
			cardsAgainstHumanity.vent.trigger("showGameSetup");
		}
	});
	new Router();
});
