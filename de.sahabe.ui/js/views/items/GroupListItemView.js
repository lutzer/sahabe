define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'utils',
	'models/GroupModel',
	'text!templates/items/groupListItemTemplate.html',
], function($, _, Marionette, vent, Utils, GroupModel, groupListItemTemplate){
	
	var GroupListItemView = Marionette.ItemView.extend({
		
		template: _.template(groupListItemTemplate),
		
		className: 'group-item',
		tagName: 'li',
		
		events: {
			'mouseenter'  : 'onHover',
			'mouseleave'  : 'onHover',
			'click #editButton' : 'onEditButtonPress'
		},
		
		modelEvents: {
			"change": "render"
		},
		
		templateHelpers: function() {
			return {
				trimString : Utils.trimString
			};

		},
		
		onHover: function(event) {
			if (event.type == 'mouseenter')
				this.$el.addClass('hover');
			else 
				this.$el.removeClass('hover');
		},
		
		onEditButtonPress: function() {
			this.trigger('edit',this.model);
			vent.trigger('open:editGroup',this.model);
		}
		
	});
	// Our module now returns our view
	return GroupListItemView;
	
});