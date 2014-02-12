$(function(){
	var Router = Backbone.Router.extend({
		initialize: function(){
			this.listenTo(cardsAgainstHumanity.vent, "navigate", this.navigateTo);
		},

		routes: {
			"game/:id/currentRound": "gameCurrentRound",
			"game/:id/players": "gamePlayers",
			"game/:id/chat": "gameChat",
			"game/:id/previousRounds": "gamePreviousRounds",
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

		gameCurrentRound: function(id){
			this.game(id);
			cardsAgainstHumanity.vent.trigger("showGame:currentRound", id);
		},

		gamePlayers: function(id){
			this.game(id);
			cardsAgainstHumanity.vent.trigger("showGame:players", id);
		},

		gameChat: function(id){
			this.game(id);
			cardsAgainstHumanity.vent.trigger("showGame:chat", id);
		},

		gamePreviousRounds: function(id){
			this.game(id);
			cardsAgainstHumanity.vent.trigger("showGame:previousRounds", id);
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
