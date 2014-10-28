define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'vent',
	'behaviors/ValidationBehavior',
	'behaviors/KeypressBehavior',
	'text!templates/overlays/linkEditTemplate.html'
], function($, _, Backbone, Marionette, vent, ValidationBehavior, KeypressBehavior, linkEditTemplate ){
	var LinkEditView = Marionette.ItemView.extend({
		
		template: _.template(linkEditTemplate),
		
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
			_.defer(function(){ self.$('#link_title').focus(); });
			
		},
		
		initialize: function(options) {
			this.oldModel = options.model.clone();
		},
		
		behaviors: {
		    validationBehaviour: {
		        behaviorClass: ValidationBehavior,
		        idPrefix: "link_"
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
				title : $('#link_title').val(),
				url : $('#link_url').val(),
				description : $('#link_description').val(),
			};
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
						vent.trigger("display:message","Link saved.");
						self.destroy();
					},
					//TODO: need to return model attributes in response
					error: function(model,error) {
						vent.trigger("display:message","Could not save link");
					}
				});
				
			} else {
				vent.trigger("display:message","Link data invalid.");
			}
			
			
		},
		
	});
	return LinkEditView;
});