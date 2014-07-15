define([
	'jquery',
	'underscore',
	'views/BaseView'
], function($, _, BaseView){
	
	var BaseListView = BaseView.extend({
		
		initialize: function() {
			
			//listen to the collections change events
			this.listenTo(this.collection, 'add', this.addOne);
			this.listenTo(this.collection, 'reset', this.addAll);
			this.listenTo(this.collection, 'remove', this.removeOne);
			
			BaseView.prototype.initialize.call(this);
		},
		
		// add all views for collection
		addAll: function() {
			this.collection.each(this.addOne);
		},
		
		// add only one model to collection
		addOne: function(model) {
			throw "Exception: ListView must implement addOne Method.";
			//this.append(new LinkListItemView({model: model}),".linklist");
		},
		
		removeOne: function(model) {
			model.destroy();
		}
	});
	// Our module now returns our view
	return BaseListView;
	
});