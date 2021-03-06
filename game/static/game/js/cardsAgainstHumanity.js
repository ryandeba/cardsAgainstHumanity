$(function(){

	//var game;

	cardsAgainstHumanity = new Backbone.Marionette.Application();

	cardsAgainstHumanity.addRegions({
		main: "#main"
	});

	cardsAgainstHumanity.on("initialize:after", function(options){
		storePlayerHash(options.playerhash);
		initUser($("#username").val());
		game = new cardsAgainstHumanity.Game();

		this.listenTo(this.vent, "showGameSetup", showGameSetup);
		this.listenTo(this.vent, "showGame", showGame);
		this.listenTo(this.vent, "showAbout", showAbout);
		this.listenTo(this.vent, "showLobby", showLobby);
		this.listenTo(this.vent, "createGame", ajaxCreateGame);
		this.listenTo(this.vent, "submitMessage", ajaxSubmitMessage);
		Backbone.history.start();
	});

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

	var showGameSetup = function(){
		var gameSetupView = new cardsAgainstHumanity.GameSetupView();
		cardsAgainstHumanity.main.show(gameSetupView);
	};

	var showGame = function(id){
		if (game.get("id") != id){
			game.set("id", id);
			var gameLayout = new cardsAgainstHumanity.GameLayout({ model: game });
			cardsAgainstHumanity.main.show(gameLayout);
		}
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

	var ajaxCreateGame = function(data){
		$.ajax({
			url: "/newGame",
			data: data,
			success: function(response){ cardsAgainstHumanity.vent.trigger("navigate", "game/" + response.id); }
		});
	};

	var ajaxSubmitMessage = function(data){
		$.ajax({
			url: "/game/" + game.get("id") + "/submitMessage",
			data: data,
			success: function(response){
				game.load(); //TODO: fix this
			}
		});
	};

});
