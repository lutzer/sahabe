define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'vent',
	'values/constants',
	'models/LinkModel',
	'behaviors/ValidationBehavior',
	'text!templates/overlays/linkAddTemplate.html'
], function($, _, Backbone, Marionette, vent, constants, LinkModel, ValidationBehavior, linkAddTemplate ){
	var LinkAddView = Marionette.ItemView.extend({
		
		template: _.template(linkAddTemplate),
		
		className: 'overlay-background',
		
		events : {
			'click .closeButton' : 'onCloseButtonPress',
			'click .saveButton' : 'onSaveButtonPress',
			'keyup input' : 'onInputEnterPress',
			'keyup .input-field' : 'onFormUpdate',
			'input .input-field' : 'onFormUpdate'
		},
	
		initialize: function() {
			this.model = new LinkModel();
		},
		
		behaviors: {
		    validationBehaviour: {
		        behaviorClass: ValidationBehavior,
		        idPrefix: "link_"
		    }
		},
		
		onRender : function() {
			var self = this;
			_.defer(function(){ 
				self.$('#link_url').focus(); 
				self.$('#link_url').select();
			});
			
		},
		
		onFormUpdate : function(event) {
			
			if (this.isDestroyed)
				return false;
			
			var data = {
				title : $('#link_title').val(),
				url : $('#link_url').val(),
			};
			this.model.set(data);
			this.triggerMethod('validateForm',event);

		},
			
		onCloseButtonPress: function() {
			this.destroy();
		},
		
		onSaveButtonPress: function() {
			
			var self = this;
			this.onFormUpdate();
			
			if (this.model.isValid()) {
				this.model.save(this.model.attributes,{
					success: function() {
						self.collection.add(self.model);
						vent.trigger('display:message','Link added.');
						self.destroy();
					},
					error: function() {
						vent.trigger('display:message','Link could not be added.');
					}
				});
			} else {
				vent.trigger('display:message','Link data is invalid');
			}
			
		},
		
		onInputEnterPress: function(e) {
			if (!e) e = window.event;
		    var keyCode = e.keyCode || e.which;
		    if (keyCode == '13'){ //enter press
		    	this.onSaveButtonPress();
		    	return false;
		    }
		    if (e.keyCode == 27) { //esc press
				this.onCloseButtonPress();
				return false;
			}
		}
		
	});
	return LinkAddView;
});