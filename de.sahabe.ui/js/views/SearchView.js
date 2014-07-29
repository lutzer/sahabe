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
			this.searchString = options.searchString;
			if (this.searchString != "")
				this.displaySearchResults(this.searchString);
			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			var compiledTemplate = _.template( searchTemplate, {searchString : this.searchString} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			
			this.assign(new LinkListView({ collection: this.collection}), ".links");
			
			return this;
		},
		
		displaySearchResults: function(searchString) {
			//get data from server
			this.collection.fetch({ data: { searchValue: searchString}, type: "POST" });
			//update hash
			history.pushState(null, null, '#/search/'+searchString);
		},
		
		_onSearchFieldValueChange: function() {
			var newSearchString = $("#searchField").val();
			if (newSearchString != this.searchString) { 
				// only fetch if the new search text is different from the previous
				this.searchString = newSearchString;
				this.displaySearchResults(this.searchString);
			}	
		}
	});
	return SearchView;
});