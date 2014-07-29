define([
	'underscore',
	'backbone',
], function(_, Backbone){
	var BaseView = Backbone.View.extend({
		
		id: 'view',
		
		initialize: function(args) {
			this.childviews = [];
			Backbone.View.prototype.initialize.call(this);
		},
		
		//assigns a subview
		assign : function (view, selector) {
			this.addChildView(view);
		    view.setElement(this.$(selector)).render();
		},
		
		//appends one subview
		append : function (view, selector) {
			this.addChildView(view);
			this.$(selector).append(view.render().el);
		},
		
		//appends many subviews
		appendMultiple : function(views, selector) {
			var container = document.createDocumentFragment();
			
			// render each subview into the container
			_.each(this._views, function(subview) {
				this.addChildView(subview);
				container.appendChild(subview.render().el)
			});
			
			//append whole container
			this.$(selector).append(container);
		},
		
		close: function() {
			//close subviews
			while(this.childviews.length > 0) {
				this.childviews.pop().close();
			}
			//close view
			this.remove();
			this.unbind();
		},
		
		//adds a childview, which will be deletet on close()
		addChildView: function(view) {
			if (!(_.contains(this.childviews,view))) //only add subview if its not alread added
				this.childviews.push(view);
		}
	
	});
	return BaseView;
});