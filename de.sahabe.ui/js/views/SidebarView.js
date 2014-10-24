define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'text!templates/sidebarTemplate.html'
], function($, _, Marionette, constants, sidebarTemplate){
	
	var SidebarView = Marionette.ItemView.extend({
		
		template : _.template(sidebarTemplate),
		
	});
	// Our module now returns our view
	return SidebarView;
	
});