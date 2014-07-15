define([
	'jquery',
	'underscore',
	'views/lists/BaseListView',
	'models/LinkCollection',
	'views/items/LinkListItemView',
	'text!templates/lists/linkListTemplate.html'
], function($, _, BaseListView, LinkModel, LinkListItemView, linkListTemplate){
	
	var LinkListView = BaseListView.extend({

		render: function(){
			
			var compiledTemplate = _.template( linkListTemplate, {} );
			this.$el.html( compiledTemplate );
			return this;
		},
		
		addOne: function(model) {
			this.append(new LinkListItemView({model: model}),".linklist");
		},
		
	});
	// Our module now returns our view
	return LinkListView;
	
});