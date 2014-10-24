define([
	'jquery',
	'underscore',
	'backbone',
	'marionette',
	'controller'
], function($, _, Backbone, Marionette, Controller) {
	
	var App = new Backbone.Marionette.Application();

	var initialize = function(){
		
		App.addRegions({
			containerRegion: "#container",
			messageRegion: "#message"
		});
		
		App.addInitializer(function(options){
			  Backbone.history.start();
		});
		
		App.Router = new Marionette.AppRouter({
			controller: new Controller(App),
			appRoutes: {
				'login' : 'login',
				'logout' : 'logout',
				'signup' : 'signup',
				'home' : 'home',
				'error/:errorId' : 'error',
				'*actions' : 'home'
			}
		});
		
		App.start();
		
	};
	
	
	//setup credentials to allow cross origin access
	/*$.ajaxSetup({
		cache: false,
		crossDomain: true,
		xhrFields: {
	        withCredentials : true
	    }
	    //timeout: 2000
	});
	$.support.cors=true;*/
	

	return {
		initialize: initialize,
	};
	
});