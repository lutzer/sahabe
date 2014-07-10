define([
	'jquery',
	'underscore',
	'backbone'
], function($, _, Backbone){

	var AppRouter = Backbone.Router.extend({
		routes: {
			'*actions' : 'default'
		},
	});
	
	// adds all views to #container and removes unused views
	var AppView = {
			showView: function(view) {
				if (this.currentView){
					this.currentView.close();
				}
				this.currentView = view;
				this.currentView.render();
				$("#container").append(this.currentView.el);
			}
	};

	var initialize = function(){
		
		//setup routes
		var app_router = new AppRouter;
		app_router.on('route:default', function(actions){
			alert("home view")
			//AppView.showView(new HomeView());
		});

		Backbone.history.start();
	};

	return {
		initialize: initialize
	};
});