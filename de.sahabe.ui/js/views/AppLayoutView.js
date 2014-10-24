define([
	'jquery',
	'underscore',
	'marionette',
	'views/SidebarView',
	'views/HeaderView',
	'views/lists/LinkListView',
	'text!templates/appLayoutTemplate.html'
], function($, _, Marionette, SidebarView, HeaderView, LinkListView, appLayoutTemplate){
	
	var AppLayoutView = Marionette.LayoutView.extend({
		
		template: _.template(appLayoutTemplate),
		
		initialize: function(options) { 
			
		},
		
		regions: {
			   'sidebarRegion': '#sidebar',
			   'contentRegion': '#content',
			   'headerRegion' : '#header'
		},
		
		onRender : function() {
			this.sidebarRegion.show(new SidebarView());
			this.headerRegion.show(new HeaderView());
			this.contentRegion.show(new LinkListView());
		}

	});
	return AppLayoutView;
	
});