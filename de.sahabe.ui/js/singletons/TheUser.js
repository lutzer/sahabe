define([
        'models/UserModel'
	], function (UserModel) {
	
	var instance = null;
	 
    function TheUser(){
        if(instance !== null){
            throw new Error("Cannot instantiate more than one TheUser, use TheUser.getInstance()");
        } 
        
        this.initialize();
    }
    
    TheUser.prototype = {
        initialize: function(){
            //Initializes the singleton.
            this.model = new UserModel();
        }
    };
    
    TheUser.getInstance = function(){
    	
        //Gets an instance of the singleton. It is better to use 
        if(instance === null){
            instance = new TheUser();
        }
        return instance;
    };
 
    return TheUser.getInstance();
});