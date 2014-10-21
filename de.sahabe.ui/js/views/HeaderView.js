define([
	'underscore',
	'backbone',
	'marionette',
	'text!templates/headerTemplate.html'
], function(_, Backbone, Marionette, headerTemplate){
	var HeaderView = Marionette.View.extend({
		//template: _.template(headerTemplate, {}),
		
		render: function() {
			var compiledTemplate = _.template( headerTemplate, {});
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	return HeaderView;
});