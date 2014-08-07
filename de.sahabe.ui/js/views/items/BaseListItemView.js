define([
	'jquery',
	'underscore',
	'views/BaseView',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html'
], function($, _, BaseView, LinkModel, linkListItemTemplate){
	
	var BaseListItemView = BaseView.extend({
		
		initialize: function() {
			this.listenTo(this.model, 'destroy', this.close);
			BaseView.prototype.initialize.call(this);
		},
	
	});
	// Our module now returns our view
	return BaseListItemView;
	
});