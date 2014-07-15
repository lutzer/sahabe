define([
        'models/UserModel'
	], function (UserModel) {
	
	var instance = null;
	 
    function TheUser(){
        if(instance !== null){
            throw new Error("Cannot instantiate more than one Singleton, use TheUser.getInstance()");
        } 
        
        this.initialize();
    }
    TheUser.prototype = {
        initialize: function(){
            this.model = new UserModel;
        }
    };
    TheUser.getInstance = function(){
        if(instance === null){
            instance = new TheUser();
        }
        return instance;
    };
 
    return TheUser;
});