define([
	'jquery',
	'underscore',
	'marionette',
	'utils',
	'vent',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html',
], function($, _, Marionette, Utils, vent, LinkModel, linkListItemTemplate){
	
	var LinkListItemView = Marionette.ItemView.extend({
		
		template: _.template(linkListItemTemplate),
		
		className: 'link-item',
		
		events: {
			'click .editButton' : '_onEditButtonClick',
			'mouseenter'  : '_onHoverLink',
			'mouseleave'  : '_onHoverLink'
		},
		
		modelEvents: {
			"change": "render"
		},
		
		initialize: function(options) {
			this.$el.attr("draggable", "true");
		},
		
		templateHelpers: function() {
			return {
				trimString : Utils.trimString,
				timeSince : Utils.timeSince
			};

		},
	
		_onEditButtonClick: function() {
			this.trigger('edit',this.model);
		},
		
		_onHoverLink: function(event) {
			if (event.type == 'mouseenter')
				this.$el.addClass('hover');
			else 
				this.$el.removeClass('hover');
		}
		
		
	});
	// Our module now returns our view
	return LinkListItemView;
	
});