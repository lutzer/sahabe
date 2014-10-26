define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'views/lists/GroupListView',
	'text!templates/sidebarTemplate.html'
], function($, _, Marionette, constants, GroupListView, sidebarTemplate){
	
	var SidebarView = Marionette.LayoutView.extend({
		
		template : _.template(sidebarTemplate),
		
		initialize: function(options) {
			this.groupCollection = options.groupCollection;
		},
		
		regions: {
			   'groupRegion': '#group-container',
		},
		
		events: {
			'click #logoutButton' : '_onClickLogoutButton',
			'click #importButton' : '_onClickImportButton'
		},
	
		_onClickLogoutButton : function() {
			window.location = "#logout";
		},
		
		_onClickImportButton : function() {
			this.trigger("open:importFile");
		},
		
		onRender : function() {
			var groupListView = new GroupListView({collection : this.groupCollection});
			this.groupRegion.show(groupListView);
		}
		
	});
	// Our module now returns our view
	return SidebarView;
	
});