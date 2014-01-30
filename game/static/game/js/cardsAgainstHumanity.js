$(function(){

	cardsAgainstHumanity = new Backbone.Marionette.Application();

	cardsAgainstHumanity.addRegions({
		main: "#main"
	});

	cardsAgainstHumanity.on("initialize:after", function(options){
		showLobby();

		this.listenTo(this.vent, "login", function(data){
			$.ajax({
				url: "/login",
				type: "POST",
				data: data,
				error: loginErrorResponse,
				success: loginSuccessResponse
			});
		});

		this.listenTo(this.vent, "register", function(data){
			$.ajax({
				url: "/register",
				type: "POST",
				data: data,
				success: registerSuccessResponse
			});
		});
	});

	var loginErrorResponse = function(response){
	};

	var loginSuccessResponse = function(response){
	};

	var registerSuccessResponse = function(response){
	};

	var showLogin = function(){
		var loginView = new cardsAgainstHumanity.LoginView();
		cardsAgainstHumanity.main.show(loginView);
	};

	var showAbout = function(){
		var aboutView = new cardsAgainstHumanity.AboutView();
		cardsAgainstHumanity.main.show(aboutView);
	};

	var showLobby = function(){
		var lobbyView = new cardsAgainstHumanity.LobbyView();
		cardsAgainstHumanity.main.show(lobbyView);
	};

});
