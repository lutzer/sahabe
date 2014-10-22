define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'singletons/User',
	'text!templates/loginTemplate.html'
], function($, _, Marionette, constants, User, loginTemplate){
	
	var LoginView = Marionette.View.extend({
		
		events : {
			'click .loginButton' : '_onClickLoginButton'
		},

		render: function(){
			var compiledTemplate = _.template( loginTemplate, {} );
			this.$el.html( compiledTemplate );
			return this;
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
				self.trigger('display:message',"Logged in.");
			};
			
			function onError() {
				self.trigger('display:error',1);
				
			}
		}
		
	});
	// Our module now returns our view
	return LoginView;
	
});