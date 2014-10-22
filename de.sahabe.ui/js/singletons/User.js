define([
        'models/UserModel'
	], function (UserModel) {
	
	var instance = null;
	 
    function User(){
        if(instance !== null){
            throw new Error("Cannot instantiate more than one Singleton, use User.getInstance()");
        } 
        
        this.initialize();
    }
    
    User.prototype = {
        initialize: function(){
            this.model = new UserModel;
        },
        
        checkLogin: function(options) {
        	var self = this;
        	//if model already fetched
        	if (this.model.isFetched)
        		options.success(self.model);
        	else {
        		// else fetch model
        		this.model.fetch({ success: function() {
        			options.success(self.model);
        		}, error: options.error });	// display error on no connection
        	}
        }
    };
    User.getInstance = function(){
        if(instance === null){
            instance = new User();
        }
        return instance;
    };
    
    return User;
});