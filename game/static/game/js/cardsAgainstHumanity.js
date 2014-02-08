$(function(){

	var game;

	cardsAgainstHumanity = new Backbone.Marionette.Application();

	cardsAgainstHumanity.addRegions({
		main: "#main"
	});

	cardsAgainstHumanity.on("initialize:after", function(options){
		storePlayerHash(options.playerhash);
		initUser($("#username").val());
		game = new cardsAgainstHumanity.Game();

		this.listenTo(this.vent, "lobby:newGame", newGame);
		this.listenTo(this.vent, "showGame", showGame);
		this.listenTo(this.vent, "showAbout", showAbout);
		this.listenTo(this.vent, "showLobby", showLobby);
		Backbone.history.start();
	});

	var newGame = function(){
		$.ajax({
			url: "/newGame",
			success: function(response){ cardsAgainstHumanity.vent.trigger("navigate", "game/" + response.id); }
		});
	};

	var storePlayerHash = function(playerhash){
		$.cookie("playerhash", playerhash, {path: "/"});
		cardsAgainstHumanity.playerhash = playerhash;
	};

	var showAbout = function(){
		var aboutView = new cardsAgainstHumanity.AboutView();
		cardsAgainstHumanity.main.show(aboutView);
	};

	var showLobby = function(){
		var lobbyGames = new cardsAgainstHumanity.LobbyGames();
		var lobbyView = new cardsAgainstHumanity.LobbyGamesView({
			collection: lobbyGames
		});
		cardsAgainstHumanity.main.show(lobbyView);
	};

	var showGame = function(id){
		game.set("id", id);
		var gameView = new cardsAgainstHumanity.GameView({
			model: game
		});
		cardsAgainstHumanity.main.show(gameView);
	};

	var initUser = function(username){
		var user = new cardsAgainstHumanity.User({
			localUsername: username,
			serverUsername: username
		});
		var userView = new cardsAgainstHumanity.UserView({
			model: user,
			el: "#form-username"
		}).render();
	};

});
