define([
	'jquery',
	'underscore',
	'views/items/BaseListItemView',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html'
], function($, _, BaseListItemView, LinkModel, linkListItemTemplate){
	
	var LinkListItemView = BaseListItemView.extend({
		
		events: {
			"click .linkDetails": "_onLinkDetailsClick",
			"click .linkDelete": "_onLinkDeleteClick",
			"change .selectBox": "_onSelectCheckbox"	
		},
		
		initialize: function() {
			this.listenTo(this.model, 'selectable', this.render);
			BaseListItemView.prototype.initialize.call(this);
		},

		render: function() {
			var compiledTemplate = _.template( linkListItemTemplate, { link : this.model.toJSON(), selectable: this.model.selectable} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onLinkDetailsClick: function() {
			//TODO: implement link details method
			console.log(this.model);
			return false;
		},
		
		_onLinkDeleteClick: function() {
			this.model.destroy();
			return false;
		},
		
		_onSelectCheckbox: function() {
			this.model.set({selected : $(".selectBox").is(":checked")});
			return false;
		}
	});
	// Our module now returns our view
	return LinkListItemView;
	
});