define([
	'jquery',
	'underscore',
	'backbone',
	'views/BaseView',
	'models/SearchModel',
	'models/LinkCollection',
	'views/lists/LinkListView',
	'text!templates/searchTemplate.html'
], function($, _, Backbone, BaseView, SearchModel, LinkCollection, LinkListView, searchTemplate){
	
	var SearchView = BaseView.extend({
		
		events: {
		    "keyup input#searchField": "_onSearchFieldValueChange"
		},
		
		initialize: function(options) {
			this.model = new SearchModel();
			
			this.searchString = options.searchString;
			if (this.searchString != "")
				this.displaySearchResults(this.searchString);
			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			var compiledTemplate = _.template( searchTemplate, {searchString : this.searchString} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			
			this.assign(new LinkListView({ collection: this.model.get('links') }), ".links");
			
			return this;
		},
		
		displaySearchResults: function(searchString) {
			//get data from server
			this.model.fetch({ data: { searchValue: searchString}, type: "GET", reset : true });
			//update hash
			if (searchString != "")
				history.pushState(null, null, '#/search/'+searchString);
			else
				history.pushState(null, null, '#/search');
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