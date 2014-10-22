define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'models/UserModel',
	'text!templates/signupTemplate.html'
], function($, _, Marionette, constants, UserModel, signupTemplate){
	
	var SignupView = Marionette.View.extend({
		
		events : {
			'click .signupButton' : '_onClickSignupButton',
			'keyup .input-field' : '_validateForm',
			'input .input-field' : '_validateForm'
		},
		
		initialize: function() {
			this.model = new UserModel();
			this.model.on("invalid", this._handleInvalidError,this);
		},

		render: function(){
			var compiledTemplate = _.template( signupTemplate, {} );
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onClickSignupButton: function() {
			var self = this;
			
			this._setValues();
			
			if (this.model.isValid()) {
				self.trigger('display:message',"Creating User Account...");
				
				this.model.signup(onSuccess,onError);
				
				function onSuccess() {
					self.trigger('display:message',"Account created");
					self.$('#message').html("Account created.");
				};
				
				function onError() {
					self.trigger('display:error',1);
				};
			} else {
				self.trigger('display:message',"User data not valid.");
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
		},200),
		
		_handleInvalidError: function(model, errors) {
			var self = this;
			console.log(errors);
			_.each(errors,function(error) {
				self.$('#'+error.attr).addClass('invalid');
			});
			
		}
		
	});
	// Our module now returns our view
	return SignupView;
	
});