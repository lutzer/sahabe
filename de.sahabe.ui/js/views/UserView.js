define([
	'jquery',
	'underscore',
	'backbone',
	'views/BaseView',
	'text!templates/userViewTemplate.html'
], function($, _, Backbone, BaseView, userViewTemplate){
	
	var UserView = BaseView.extend({
		
		initialize: function(options) {
			this.username = options.username;
			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			var compiledTemplate = _.template( userViewTemplate, {username: this.username} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	return UserView;
});