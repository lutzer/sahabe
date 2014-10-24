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
    };
    User.getInstance = function(){
        if(instance === null){
            instance = new User();
        }
        return instance;
    };
    
    return User;
});