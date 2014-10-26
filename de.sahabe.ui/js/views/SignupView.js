define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'values/constants',
	'models/UserModel',
	'text!templates/signupTemplate.html'
], function($, _, Marionette, vent, Constants, UserModel, signupTemplate){
	
	var SignupView = Marionette.ItemView.extend({
		
		template :  _.template( signupTemplate),
		className: 'single-page',
		
		events : {
			'click .signupButton' : '_onClickSignupButton',
			'click .loginButton' : '_OnClickLoginButton',
			'keyup .input-field' : '_validateForm',
			'input .input-field' : '_validateForm'
		},
		
		initialize: function() {
			this.model = new UserModel();
			this.model.on("invalid", this._handleInvalidError,this);
		},
		
		_OnClickLoginButton: function() {
			window.location = "#login"
		},
		
		_onClickSignupButton: function() {
			var self = this;
			
			this._setValues();
			
			if (this.model.isValid()) {
				vent.trigger('display:message',"Creating User Account...");
				
				this.model.signup(onSuccess,onError);
				
				function onSuccess() {
					vent.trigger('display:message',"Account created");
				};
				
				function onError(error) {
					vent.trigger('display:error',1,error);
				};
			} else {
				vent.trigger('display:message',"Form data is not valid.");
			}
		},
		
		_setValues : function() {
			var userdata = {
				username : this.$('#username').val(),
				password : this.$('#password').val(),
				password2 : this.$('#password2').val(),
				email : this.$('#email').val()
			};
			
			this.model.set(userdata);
		},
		
		_validateForm : _.debounce(function(event) {
			
			$('#'+event.target.id).removeClass('invalid');
			this._setValues();
			this.model.isValid();
		},Constants.settings.inputDebounceTime),
		
		_handleInvalidError: function(model, errors) {
			var self = this;
			_.each(errors,function(error) {
				self.$('#'+error.attr).addClass('invalid');
			});
			
		}
		
	});
	// Our module now returns our view
	return SignupView;
	
});