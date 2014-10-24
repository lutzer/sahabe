define([
	'jquery',
	'underscore',
	'backbone',
	'marionette',
	'models/LinkCollection',
	'views/items/LinkListItemView',
], function($, _, Backbone, Marionette, LinkCollection, LinkListItemView){
	
	var LinkListView = Backbone.Marionette.CollectionView.extend({
		
		childView: LinkListItemView,
		
		className: "link-list"
		
		
		
	});
	// Our module now returns our view
	return LinkListView;
	
});