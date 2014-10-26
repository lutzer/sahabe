define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'values/constants',
	'models/UserModel',
	'behaviors/ValidationBehavior',
	'text!templates/signupTemplate.html'
], function($, _, Marionette, vent, constants, UserModel, ValidationBehavior, signupTemplate){
	
	var SignupView = Marionette.ItemView.extend({
		
		template :  _.template( signupTemplate),
		className: 'single-page',
		
		events : {
			'keyup .input-field' : 'onFormUpdate',
			'input .input-field' : 'onFormUpdate'
		},
		
		triggers : {
			'click .signupButton' : 'clickSignupButton',
			'click .loginButton' : 'clickLoginButton'
		},
		
		initialize: function() {
			this.model = new UserModel();
		},
		
		behaviors: {
		    validationBehaviour: {
		        behaviorClass: ValidationBehavior
		    }
		},
		
		onClickLoginButton: function() {
			window.location = "#login"
		},
		
		onClickSignupButton: function() {
			
			this.onFormUpdate();
			
			if (this.model.isValid()) {
				vent.trigger('display:message',"Creating User Account...");
				
				this.model.signup(onSuccess,onError);
				
				function onSuccess() {
					vent.trigger('display:message',"Account created");
					window.location = "#login";
				};
				
				function onError(error) {
					vent.trigger('display:error',1,error);
				};
			} else {
				vent.trigger('display:message',"Form data is not valid.");
			}
		},
		
		onFormUpdate : function(event) {
			
			var userdata = {
				username : this.$('#username').val(),
				password : this.$('#password').val(),
				password2 : this.$('#password2').val(),
				email : this.$('#email').val()
			};
			
			this.model.set(userdata);
			this.triggerMethod('validateForm',event);

		}
		
	});
	// Our module now returns our view
	return SignupView;
	
});