define([
	'jquery',
	'underscore',
	'marionette',
	'utils',
	'models/GroupModel',
	'text!templates/items/groupListItemTemplate.html',
], function($, _, Marionette, Utils, GroupModel, groupListItemTemplate){
	
	var GroupListItemView = Marionette.ItemView.extend({
		
		template: _.template(groupListItemTemplate),
		
		className: 'group-item',
		tagName: 'li',
		
		templateHelpers: function() {
			return {
				trimString : Utils.trimString
			};

		}
	});
	// Our module now returns our view
	return GroupListItemView;
	
});