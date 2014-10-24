define([
	'underscore',
	'backbone',
	'marionette',
	'values/constants'
], function(_, Backbone, Marionette,Constants){
	var MessageView = Marionette.ItemView.extend({
		
		className: "message-text",

		template: _.template("<%= message %>"),
		
		timeout: Constants.settings.messageDisplayTimeout,
		
		initialize: function(options) {
			if (options.hasOwnProperty('message'))
				this.message = options.message;
			
			if (options.hasOwnProperty('timeout'))
				this.timeout = options.timeout;
				
		},
		
		
		templateHelpers : function() {
			return { message : this.message };
		},
		
		onRender: function(){
			var self = this;
			setInterval(function() {
				self.destroy();
			},this.timeout);
			
		}
		
	});
	return MessageView;
});