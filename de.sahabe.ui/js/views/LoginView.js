define([
	'jquery',
	'underscore',
	'views/BaseView',
	'values/constants',
	'text!templates/loginViewTemplate.html'
], function($, _, BaseView, constants, loginViewTemplate){
	
	var LoginView = BaseView.extend({
		
		events : {
			'click #loginButton' : '_onClickLoginButton'
		},

		render: function(){
			var compiledTemplate = _.template( loginViewTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onClickLoginButton: function() {
			
			var username = $('#username').val();
			var password = $('#password').val();
			var remember = $('#remember').is(":checked");
			
			$.ajax({
	            url: constants.settings.web_service_url+"/login",
	            type: 'POST',
	            dataType: "json",
	            data: { username: username, password : password, remember : remember},
	            success: function (data) {
	                console.log("login succesfull:");
	                console.log(data);
	            },
	            error: function(error) {
	            	console.log("login failed");
	            	console.log(error);
	            }
	        });
		}
	});
	// Our module now returns our view
	return LoginView;
	
});