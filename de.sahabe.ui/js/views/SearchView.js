define([
	'jquery',
	'underscore',
	'backbone',
	'views/BaseView',
	'models/SearchCollection',
	'views/lists/LinkListView',
	'text!templates/searchTemplate.html'
], function($, _, Backbone, BaseView, SearchCollection, LinkListView, searchTemplate){
	
	var SearchView = BaseView.extend({
		
		events: {
		    "keyup input#searchField": "_onSearchFieldValueChange"
		},
		
		initialize: function(options) {
			
			this.collection = new SearchCollection();
			
			this.searchString = "";

			BaseView.prototype.initialize.call(this);

		},

		render: function(){
			var compiledTemplate = _.template( searchTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			
			this.assign(new LinkListView({ collection: this.collection}), ".links");
			
			return this;
		},
		
		_onSearchFieldValueChange: function() {
			var newSearchString = $("#searchField").val();
			if (newSearchString != this.searchString) { 
				// only fetch if the new search text is different from the previous
				this.searchString = newSearchString;
				this.collection.fetch({ data: { searchValue: this.searchString}, type: "POST" });
			}
				
		}
	});
	return SearchView;
});