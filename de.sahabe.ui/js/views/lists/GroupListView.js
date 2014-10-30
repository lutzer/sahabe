define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'models/GroupModel',
	'views/items/GroupListItemView',
	'text!templates/lists/groupListTemplate.html'
], function($, _, Marionette, vent, GroupModel, GroupListItemView, groupListTemplate){
	
	var GroupListView = Marionette.CompositeView.extend({
		
		template: _.template(groupListTemplate),
		
		childView: GroupListItemView,
		
		childViewContainer: '.group-list',
		
		events : {
			'click #addGroupButton': 'onAddGroupButtonClick',
			'click #cancelNewGroupButton': 'onCancelNewGroupButtonClick',
			'keydown #newGroupField': 'onNewGroupFieldKeyPress'
		},
		
		initialize: function(options) {
			if (!options.collection.fetched) {
				options.collection.fetch();
			}
				
		},
		
		onRender : function() {
			this.showCreateGroupForm(false);
		},
		
		/* Add Group Functions */
		
		onAddGroupButtonClick: function() {
			this.showCreateGroupForm(true);
		},
		
		onCancelNewGroupButtonClick: function() {
			this.showCreateGroupForm(false);
		},
		
		onNewGroupFieldKeyPress: function(e) {
			if (!e) e = window.event;
		    var keyCode = e.keyCode || e.which;
		    if (keyCode == '13'){ // enter
				this.showCreateGroupForm(false);
				var name = this.$('#newGroupField').val().trim();
				this.createGroup(name,false);
				return false;
		    }
		    if (keyCode == '27') { //esc 
		    	this.showCreateGroupForm(false);
		    	return false;
		    }
		    return true;
		},
		
		showCreateGroupForm : function(show) {
			if (show) {
				this.$('#newGroupField').val("");
				this.$('.create-group-form').show();
				this.$('#addGroupButton').hide();
				this.$('#newGroupField').focus();
			} else {
				this.$('.create-group-form').hide();
				this.$('#addGroupButton').show();
			}
		},
		
		createGroup: function(groupName,publicGroup) {
			var self = this;
			
			var group = new GroupModel({name : groupName, public: publicGroup});
			if (!group.isValid())
				vent.trigger("display:message","'" + groupName + "' is not a valid groupname");
			group.save(group.attributes,{
				success : function() {
					self.collection.add(group);
					vent.trigger("display:message","Group "+ groupName + " created.")
				},
				error: function() {
					group.destroy();
					vent.trigger("display:message","Error creating group")
			}});
		}
		
	});
	// Our module now returns our view
	return GroupListView;
	
});