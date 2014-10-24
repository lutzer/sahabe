define([
        'marionette',
        'utils',
        'singletons/User',
        'views/AppLayoutView',
        'views/LoginView',
        'views/SignupView',
        'views/ErrorView',
        'views/MessageView'
], function(Marionette, Utils, User, AppLayoutView, LoginView, SignupView, ErrorView, MessageView){
	
	var Controller = Marionette.Controller.extend({
		
		initialize: function(app) {
			this.app = app;
		},
		
		checkLogin: function(callback) {
			var self = this;
			
			var user = User.getInstance();
			user.model.checkLogin(onSuccess,onError);
			
			function onSuccess() {
				callback(true);
			};
			
			function onError(error) {
				if (error.status == 401)
					callback(false);
				else
					self.showError(1,error);
			};
		},
		
		showError: function(errorId,error) {
			if (error !== 'undefined' && Utils.propertyExists(error,"responseJSON.message"))
				this.app.containerRegion.show(new ErrorView({error : errorId, message : error.responseJSON.message}));
			else
				this.app.containerRegion.show(new ErrorView({error : errorId}));
			//window.location = "#error/"+errorId;
		},
		
		showMessage: function(message) {
			this.app.messageRegion.show(new MessageView({message : message}));
		},
			
		/* ROUTES */
		
		home: function() {
			
			var self = this;
			
			this.checkLogin(
				function(loggedIn) {
					if (loggedIn) {
						var layout = new AppLayoutView();
						self.listenTo(layout, "display:error", self.showError);
						self.listenTo(layout, "display:message", self.showMessage);
						self.app.containerRegion.show(layout);
					} else
						window.location = "#login";
				}
			);
		},
		
		login: function() {
			var view = new LoginView();
			this.listenTo(view, "display:error", this.showError);
			this.listenTo(view, "display:message", this.showMessage);
			this.app.containerRegion.show(view);
		},
		
		logout: function() {
			var self = this;
			
			var user = User.getInstance();
			user.model.logout(onSuccess,onError);
			
			function onSuccess(response) {
				self.showMessage(response.message);
				window.location="#";
			};
			
			function onError(error) {
				if (error.status != 401)
					self.showError(0,error);
				else
					window.location="#";
			};
		},
		
		signup: function() {
			var view = new SignupView();
			this.listenTo(view, "display:error", this.showError);
			this.listenTo(view, "display:message", this.showMessage);
			this.app.containerRegion.show(view);
		},
		
		user: function(name) {
			alert("Userview for "+name);
		},
		
		error: function(errorId) {
			this.app.containerRegion.show(new ErrorView({error : errorId}));
		},
		
		defaultRoute: function() {
			//window.location = "#home";
		},
		
		
		
	});
	
	return Controller;
});