define([
        'marionette',
        'singletons/User',
        'views/HomeView',
        'views/LoginView',
        'views/SignupView',
        'views/ErrorView'
], function(Marionette, User, HomeView, LoginView, SignupView, ErrorView){
	
	var Controller = Marionette.Controller.extend({
		
		initialize: function(app) {
			this.app = app;
		},
		
		checkLogin: function(callback) {
			var self = this;
			
			var user = User.getInstance();
			user.checkLogin({
				success: function() {
					callback(user.model.isLoggedIn);
				},
				error : function() {
					self.showError(1);
				}
			});
		},
		
		showError: function(errorId) {
			this.app.contentRegion.show(new ErrorView({error : errorId}));
		},
		
		showMessage: function(message) {
			$('#message').html(message);
		},
			
		/* ROUTES */
		
		home: function() {
			
			this.checkLogin(
				function(loggedIn) {
					if (loggedIn)
						return;//do code
					else
						window.location = "#login";
				}
			);
		},
		
		login: function() {
			var view = new LoginView();
			this.listenTo(view, "display:error", this.showError);
			this.listenTo(view, "display:message", this.showMessage);
			this.app.contentRegion.show(view);
		},
		
		signup: function() {
			var view = new SignupView();
			this.listenTo(view, "display:error", this.showError);
			this.listenTo(view, "display:message", this.showMessage);
			this.app.contentRegion.show(view);
		},
		
		user: function(name) {
			alert("Userview for "+name);
		},
		
		defaultRoute: function() {
			window.location = "#home";
		},
		
		
		
	});
	
	return Controller;
});