define([
	'jquery',
	'underscore',
	'views/BaseView',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html'
], function($, _, BaseView, LinkModel, linkListItemTemplate){
	
	var LinkListItemView = BaseView.extend({

		render: function(){
			var compiledTemplate = _.template( linkListItemTemplate, { link : this.model.toJSON() } );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return LinkListItemView;
	
});