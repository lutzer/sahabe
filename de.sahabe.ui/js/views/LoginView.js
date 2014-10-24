define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'singletons/User',
	'text!templates/loginTemplate.html'
], function($, _, Marionette, constants, User, loginTemplate){
	
	var LoginView = Marionette.ItemView.extend({
		
		template :  _.template( loginTemplate),
		className: 'single-page',
		
		events : {
			'click .loginButton' : '_onClickLoginButton',
			'click .signupButton' : '_onClickSignupButton'
		},

		
		_onClickLoginButton: function() {
			var self = this;
		
			var username = $('#username').val();
			var	password = $('#password').val();
			var	remember = $('#remember').is(":checked");
			
			var user = User.getInstance();
			
			user.model.login(username,password,remember,onSuccess,onError);
			
			self.trigger('display:message',"Logging in...");
			
			function onSuccess() {
				self.trigger('display:message',"Login succesfull!");
				window.location = "#";
			};
			
			function onError(error) {
				
				if (error.status == 401)
					self.trigger('display:message',error.responseJSON.message);
				else
					self.trigger('display:error',1,error);
				
			}
		},
		
		_onClickSignupButton: function () {
			window.location = "#signup";
		}
		
	});
	// Our module now returns our view
	return LoginView;
	
});