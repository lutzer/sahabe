define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'vent',
	'behaviors/ValidationBehavior',
	'behaviors/KeypressBehavior',
	'text!templates/overlays/groupEditTemplate.html'
], function($, _, Backbone, Marionette, vent, ValidationBehavior, KeypressBehavior, groupEditTemplate ){
	var GroupEditView = Marionette.ItemView.extend({
		
		template: _.template(groupEditTemplate),
		
		className: 'overlay-background',
		
		events : {
			'keyup input' : 'onInputEnterPress',
			'keyup .input-field' : 'onFormUpdate',
			'input .input-field' : 'onFormUpdate'
		},
		
		triggers : {
			'click .closeButton' : 'closeButtonPress',
			'click .saveButton' : 'saveButtonPress'
		},
		
		onRender : function() {
			var self = this;
			_.defer(function(){ self.$('#group_name').focus(); });
			
		},
		
		initialize: function(options) {
			this.oldModel = options.model.clone();
		},
		
		behaviors: {
		    validationBehaviour: {
		        behaviorClass: ValidationBehavior,
		        idPrefix: "group_"
		    },
		    keypressBehavior: {
		        behaviorClass: KeypressBehavior,
		        listenToKeys : {
		        	'13' : 'saveButtonPress',
		        	'27' : 'closeButtonPress'
		        }
		    }
		},
		
		onFormUpdate : function(event) {
			
			if (this.isDestroyed)
				return false;
			
			var data = {
				name : this.$('#group_name').val(),
				public : this.$('#group_public').is(":checked")
			};
			
			console.log(data);
			this.model.set(data);
			this.triggerMethod('validateForm',event);

		},
			
		onCloseButtonPress: function() {
			//revert model
			this.model.set(this.oldModel.attributes);
			this.destroy();
		},
		
		onSaveButtonPress: function() {
			
			var self = this;
			this.onFormUpdate();
			
			if (this.model.isValid()) {
				this.model.save(this.model.attributes,{ 
					success: function(model,response) {
						vent.trigger("display:message","Group saved.");
						self.destroy();
					},
					//TODO: need to return model attributes in response
					error: function(model,error) {
						vent.trigger("display:message","Error saving group");
					}
				});
				
			} else {
				vent.trigger("display:message","Group data invalid.");
			}
			
			
		},
		
	});
	return GroupEditView;
});