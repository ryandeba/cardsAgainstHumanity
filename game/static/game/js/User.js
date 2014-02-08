$(function(){

	cardsAgainstHumanity.User = Backbone.Model.extend({

		save: function(){
			var self = this;
			$.ajax({
				url: "setPlayerName/" + self.get("localUsername"),
				success: function(){
					self.set("serverUsername", self.get("localUsername"));
				}
			});
		}

	});

	cardsAgainstHumanity.UserView = Backbone.View.extend({
		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		},

		render: function(){
			var $submit = this.$el.find(".js-username-submit");
			if (this.model.get("localUsername") == this.model.get("serverUsername")){
				$submit.removeClass("btn-primary").addClass("btn-success").html("Saved");
			} else {
				$submit.addClass("btn-primary").removeClass("btn-success").html("Save");
			}
		},

		events: {
			"keyup #username": "usernameChanged",
			"submit": "usernameSubmit"
		},

		usernameChanged: function(){
			this.model.set("localUsername", this.$el.find("#username").val());
		},

		usernameSubmit: function(e){
			e.preventDefault();
			this.model.save();
		}
	});

});
