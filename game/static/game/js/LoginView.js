$(function(){
	cardsAgainstHumanity.LoginView = Backbone.Marionette.ItemView.extend({
		template: "#template-login",

		events: {
			"submit .js-login-form": "login",
			"click .js-register": "register"
		},

		login: function(e){
			e.preventDefault();
			cardsAgainstHumanity.vent.trigger("login", this.$el.find(".js-login-form").serialize());
		},

		register: function(){
			cardsAgainstHumanity.vent.trigger("register", this.$el.find(".js-login-form").serialize());
		}
	});
});
