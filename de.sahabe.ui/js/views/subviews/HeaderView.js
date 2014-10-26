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
			'input #searchField' : '_onSearchBarInput'
		},
		
		_onSearchBarInput:  _.debounce(function() {
			var searchText = $('#searchField').val();
			this.trigger("search:changed",searchText);
		},300)
		
	});
	return HeaderView;
});