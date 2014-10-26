define([], function(){
	
	var Utils = {
			
			//checks if property exists in the object. i.e propertyExists(obj,'prop1.subprop1')
			propertyExists: function (obj,properties) {
				
				properties = properties.split('.');
				
				for(var i=0;i<properties.length;i++) {
					if (!obj.hasOwnProperty(properties[i]))
						return false;
					
					obj = obj[properties[i]];
					if (typeof obj == 'undefined')
						return false;
				}
				return true;
			},
			
			trimString: function(str,length) {
				if (str.length > length)
					return str.substring(0,length) + '...';
				else
					return str;
			}
	
	};
	
	return Utils;
});