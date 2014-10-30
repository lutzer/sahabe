define([
        'underscore'
 ], function(_){
	
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
			},
			
			timeSince: function(date) {
				
			    var seconds = Math.floor((new Date() - new Date(date)) / 1000);
			    
			    var interval = Math.floor(seconds / 31536000);

			    if (interval > 1) {
			        return interval + " years";
			    }
			    interval = Math.floor(seconds / 2592000);
			    if (interval > 1) {
			        return interval + " months";
			    }
			    interval = Math.floor(seconds / 86400);
			    if (interval > 1) {
			        return interval + " days";
			    }
			    interval = Math.floor(seconds / 3600);
			    if (interval > 1) {
			        return interval + " hours";
			    }
			    interval = Math.floor(seconds / 60);
			    if (interval > 1) {
			        return interval + " minutes";
			    }
			    return Math.floor(seconds) + " seconds";
			},
			
			// removes http
			removeSchemeFromUrl: function(url) {
				var remove = url.match("^(https?|ftp):\\/\\/");
				return url.substr(remove[0].length,url.length);
			},
	};
	
	return Utils;
});