define([
	'jquery',
	'underscore',
	'views/BaseView',
	'models/LinkCollection',
	'views/items/LinkListItemView',
	'text!templates/lists/linkListTemplate.html'
], function($, _, BaseView, LinkModel, LinkListItemView, linkListTemplate){
	
	var LinkListView = BaseView.extend({
		
		initialize: function() {
			
			//listen to the collections change events
			this.listenTo(this.collection, 'add', this.addOne);
			this.listenTo(this.collection, 'reset', this.addAll);
			//this.listenTo(this.collection, 'all', this.render);
			
			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			
			var compiledTemplate = _.template( linkListTemplate, {} );
			this.$el.html( compiledTemplate );
			return this;
		},
		
		// add all views for collection
		addAll: function() {
			this.collection.each(this.addOne);
		},
		
		// add only one model to collection
		addOne: function(model) {
			this.append(new LinkListItemView({model: model}),".linklist");
		}
	});
	// Our module now returns our view
	return LinkListView;
	
});