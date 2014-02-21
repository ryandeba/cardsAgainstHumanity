$(function(){

	cardsAgainstHumanity.GameMessage = Backbone.Model.extend({
		defaults: {
			name: "",
			message: ""
		}
	});

	cardsAgainstHumanity.GameMessages = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GameMessage
	});

	cardsAgainstHumanity.GameMessageView = Backbone.Marionette.ItemView.extend({
		template: "#template-gamemessage",

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		}
	});

	cardsAgainstHumanity.GameMessagesView = Backbone.Marionette.CollectionView.extend({
		itemView: cardsAgainstHumanity.GameMessageView
	});

	cardsAgainstHumanity.ChatLayout = Backbone.Marionette.Layout.extend({
		template: "#template-chat",

		regions: {
			messagesRegion: "#chat-messages"
		},

		events: {
			"submit #form-message": "submitMessage"
		},

		submitMessage: function(e){
			e.preventDefault();
			var data = this.$el.find("#form-message").serialize();
			this.$el.find("#chat-message").val("");
			cardsAgainstHumanity.vent.trigger("submitMessage", data);
		},

		onRender: function(){
			var self = this;
			if (_.isUndefined(self.messagesRegion.currentView)){
				self.messagesRegion.show(new cardsAgainstHumanity.GameMessagesView({ collection: self.collection }));
			}
		}
	});

});
