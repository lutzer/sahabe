define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'text!templates/headerTemplate.html'
], function($, _, Backbone, Marionette, headerTemplate){
	var HeaderView = Marionette.ItemView.extend({
		
		template: _.template(headerTemplate),
		
		events: {
			'keyup #searchField' : '_onSearchBarInput',
			'input #searchField' : '_onSearchBarInput',
			'click #addLinkButton' : '_onAddLinkButtonClick'
		},
		
		_onSearchBarInput:  _.debounce(function() {
			var searchText = $('#searchField').val().trim();
			this.trigger("search:changed",searchText);
			
			/*if (searchText != "")
				history.pushState(null, null, '#/search/'+searchText);
			else
				history.pushState(null, null, '#/search');*/
			
		},300),
		
		onRender : function() {
			var self = this;
			_.defer(function(){ self.$('#searchField').focus(); });
		},
		
		_onAddLinkButtonClick: function() {
			this.trigger("open:addLink");
		}
		
	});
	return HeaderView;
});