define([
	'jquery',
	'underscore',
	'views/lists/BaseListView',
	'models/LinkCollection',
	'views/items/LinkListItemView',
	'text!templates/lists/linkListTemplate.html'
], function($, _, BaseListView, LinkModel, LinkListItemView, linkListTemplate){
	
	var LinkListView = BaseListView.extend({
		
		subviews : [],
		
		render: function(){
			
			var compiledTemplate = _.template( linkListTemplate, {} );
			this.$el.html( compiledTemplate );
			return this;
		},
		
		afterReset: function(attributes, options) {
			var self = this;
			
			// remove previous model views
			/*_.each(this.subviews, function(view) {
				view.close();
			});*/
			_.each(options.previousModels, function(model) {
				self.removeOne(model);
			});
			
			// add new model views
			this.subviews = [];
			this.collection.each( function(model) {
				self.subviews.push(new LinkListItemView({model: model}));
			});
			this.appendMany(this.subviews,".linklist");
			
			//update result number
			this.updateLinkCount();
		},
		
		addOne: function(model) {
			this.append(new LinkListItemView({model: model}),".linklist");
		},
		
		updateLinkCount: function() {
			$(".linksFound").html(this.collection.length);
		}
		
	});
	// Our module now returns our view
	return LinkListView;
	
});