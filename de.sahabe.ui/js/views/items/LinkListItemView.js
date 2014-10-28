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
			'click #editButton' : 'onEditButtonClick',
			'click #deleteButton' : 'onDeleteButtonClick',
			'mouseenter'  : 'onHoverLink',
			'mouseleave'  : 'onHoverLink'
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
	
		onEditButtonClick: function() {
			vent.trigger('open:editLink',this.model);
			//this.trigger('edit',this.model);
		},
		
		onDeleteButtonClick: function() {
			console.log('click');
			//this.$('#deleteButton').addClass('ask-permission');
			//this.$('#deleteButton').attr('value','Yes');
			this.model.destroy({
				success: function() {
					vent.trigger('display:message',"Link deleted.");
				}, 
				error: function() {
					vent.trigger('display:message',"Cloud not delete link");
				}
			});
		},
		
		onHoverLink: function(event) {
			if (event.type == 'mouseenter')
				this.$el.addClass('hover');
			else 
				this.$el.removeClass('hover');
		}
		
		
	});
	// Our module now returns our view
	return LinkListItemView;
	
});