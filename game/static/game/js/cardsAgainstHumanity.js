$(function(){

	cardsAgainstHumanity = new Backbone.Marionette.Application();

	cardsAgainstHumanity.addRegions({
		main: "#main"
	});

	cardsAgainstHumanity.on("initialize:after", function(options){
		storePlayerHash();
		showLobby();
	});

	var storePlayerHash = function(){
		$.cookie("playerhash", $("#playerhash").val(), {path: "/"});
	};

	var showAbout = function(){
		var aboutView = new cardsAgainstHumanity.AboutView();
		cardsAgainstHumanity.main.show(aboutView);
	};

	var showLobby = function(){
		lobbyGames = new cardsAgainstHumanity.LobbyGames();
		var lobbyView = new cardsAgainstHumanity.LobbyGamesView({
			collection: lobbyGames
		});
		cardsAgainstHumanity.main.show(lobbyView);
	};

});
