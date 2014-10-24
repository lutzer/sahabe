define([
	'underscore',
	'backbone',
	'marionette',
	'text!templates/headerTemplate.html'
], function(_, Backbone, Marionette, headerTemplate){
	var HeaderView = Marionette.ItemView.extend({
		
		template: _.template(headerTemplate),
		
	});
	return HeaderView;
});