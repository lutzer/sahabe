define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'views/lists/GroupListView',
	'text!templates/sidebarTemplate.html',
	'text!templates/sidebarTemplate_collapsed.html'
], function($, _, Marionette, constants, GroupListView, sidebarTemplate, sidebarTemplate_collapsed){
	
	var SidebarView = Marionette.LayoutView.extend({
		
		// is the view collapsed?
		collapsed : false,
		
		initialize: function(options) {
			this.groupCollection = options.groupCollection;
		},
		
		regions: {
			   'groupRegion': '#group-container',
			   'userRegion': '#user-container'
		},
		
		events: {
			'click #logoutButton' : 'onClickLogoutButton',
			'click #importButton' : 'onClickImportButton',
			'click #collapseViewButton' : 'onCollapse',
			'click #expandViewButton' : 'onExpand'
		},
		
		// load subviews if expanded
		onRender : function() {
			if (!this.collapsed) {
				var groupListView = new GroupListView({collection : this.groupCollection});
				this.groupRegion.show(groupListView);
			}
		},
		
		// load template for collapsed or expanded view
		getTemplate: function(){
		    if (!this.collapsed)
		      return _.template(sidebarTemplate);
		    else
		      return _.template(sidebarTemplate_collapsed);
		  },
	
		onClickLogoutButton : function() {
			window.location = "#logout";
		},
		
		onClickImportButton : function() {
			this.trigger("open:importFile");
		},
		
		onCollapse: function() {
			var self = this;
			
			this.trigger('collapse');
			this.collapsed = true;
			setTimeout(function() {
				self.render();
			},250);
		},
		
		onExpand: function() {
			var self = this;
			this.trigger('expand');
			this.collapsed = false;
			self.render();
		}
		
	});
	// Our module now returns our view
	return SidebarView;
	
});