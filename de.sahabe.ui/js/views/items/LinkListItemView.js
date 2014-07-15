define([
	'jquery',
	'underscore',
	'views/items/BaseListItemView',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html'
], function($, _, BaseListItemView, LinkModel, linkListItemTemplate){
	
	var LinkListItemView = BaseListItemView.extend({
		
		events: {
			"click .linkDetails": "_onLinkDetailsClick"
		},

		render: function() {
			var compiledTemplate = _.template( linkListItemTemplate, { link : this.model.toJSON() } );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onLinkDetailsClick: function() {
			console.log(this.model);
			return false;
		}
	});
	// Our module now returns our view
	return LinkListItemView;
	
});