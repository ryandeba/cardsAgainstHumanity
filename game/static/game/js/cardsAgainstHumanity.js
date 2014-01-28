$(function(){

	cardsAgainstHumanity = new Backbone.Marionette.Application();

	cardsAgainstHumanity.addRegions({
		main: "#main"
	});

	cardsAgainstHumanity.on("initialize:after", function(options){
		showLogin();
	});

	var showLogin = function(){
		loginView = new LoginView();
		cardsAgainstHumanity.main.show(loginView);
	};

	var LoginView = Backbone.Marionette.ItemView.extend({
		template: "#template-login"
	});

});
