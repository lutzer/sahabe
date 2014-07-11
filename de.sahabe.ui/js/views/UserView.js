define([
	'jquery',
	'underscore',
	'backbone',
	'views/BaseView',
	'models/LinkCollection',
	'views/lists/LinkListView',
	'text!templates/userTemplate.html'
], function($, _, Backbone, BaseView, LinkCollection, LinkListView, userTemplate){
	
	var UserView = BaseView.extend({
		
		initialize: function(options) {
			this.username = options.username;
			
			this.collection = new LinkCollection();
			this.collection.fetch();

			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			var compiledTemplate = _.template( userTemplate, {username: this.username} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			
			this.assign(new LinkListView({ collection: this.collection}), ".links");
			
			return this;
		}
	});
	return UserView;
});