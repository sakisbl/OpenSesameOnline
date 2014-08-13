/**
* Utilities namespace
* Contains utilities used throughout all of the javascript OpenSesame engine
*/
utils = {

	/**
	* Shuffle function.
	* @param array - the array to be shuffled
	* @return - the shuffled array
	*/
    shuffle: function(array) {
        var el = array.length, t, i;

        // While there remain elements to shuffle
        while (el) {
	        // Pick a remaining element
	        i = Math.floor(Math.random() * el--);

	        // And swap it with the current element.
	        t = array[el];
	        array[el] = array[i];
	        array[i] = t;
        }
        return array;
    },

    /**
    * AlignCenter function.
    * @param object - Fabric object that is set to be in the center of the CANVAS.
    */
    alignCenter: function (object) {
        object.set( {
            left: CANVAS.getWidth() / 2 - object.getWidth()/2, 
            top: CANVAS.getHeight() / 2 - object.getHeight()/2
        });
    },

    /**
    * CanvasColor function. Colors canvas and the surrounding body
    * @param color - the new background color of the canvas and the surrounding container
    */
    canvasColor: function(color) {
        CANVAS.setBackgroundColor(color);
        $('body').css({'background-color': color});
    },

    /**
    * Canvas initial placement function.
    * Makes sure the canvas is placed in the center 
    * of the screen and has the same dimensions as how 
    * it was declared in the OS script.
    * @param width - the width this experiment was created in
    * @parm height - the height this experiment was created in
    */
    canvasInit: function (width, height) {
        var canvasNode = document.getElementById('canvas');
        canvasNode.width = width;
        canvasNode.height = height;
        canvasNode.style.marginLeft =  ((screen.width/2) - width / 2).toString() + "px";
        canvasNode.style.marginTop = ((screen.height/2) - height / 2).toString() + "px";
    },

    /**
    * Restores the Canvas. 
    * Every object that can draw something on the canvas will call this function
    * before drawing. This has to be done so two objects will not have interference 
    * when updating the canvas with a backgroundcolor or with something else that is drawn on it.
    * @param backgroundColor - background color of Canvas
    */
    canvasPrepare: function (backgroundColor) {
    	this.canvasColor(backgroundColor);
    	CANVAS.clear();
    },

    /**
    * Checks if item is last in the experiment
    * If so, the parent has to automatically be notified of this, instead of 
    * waiting for user input. (Notifying the parent is done in Experiment.js)
    * Can only detect if last item 
    * is not a loop, sequence or reset_feedback. Reset_feedback does not have to be
    * checked, because it will automatically skip to the next item when it is called.
    * (This solution is not ideal and was still in development)
    *
    * @param item - the item to be checked
    * @return - true if item was last in the experiment, false otehrwise
    */
    isLast: function(item) {
        if (item instanceof loop || item instanceof sequence || item instanceof reset_feedback) {
            return false;
        }
        var parent = item.getParent();
        if (parent.getObjectCounter() == parent.getObjects().length - 1) {
            if(parent.getParent() instanceof Experiment) {
                return true;
            }
        }
        return false;
    },

    /**
    * This function checks if there is a variable present in the string.
    * If so, the variable will be replaced by its actual value that is in globalVars.
    * @variable the value to be parsed
    * @return the parsed string
    */
    parseVar: function (variable) {
        //If a variable is not of type string, it can never contain an opensesame variable of type "[varname]"
        if (!(typeof variable == "string")) {
            return variable;
        }

        //This regular expression will find all occurences of "[varname]" in a string
    	var regExp = /\[\w+\]/g; 

    	//String.match() creates an array of matches it's found. If there are none, it returns null.
    	var match = variable.match(regExp);
    
    	//For every match found, the variable name in the original string will be replaced by 
    	//its value that is in globalVars[]. We have to add a recursive call inside the for-loop
    	//incase a variable is defined in terms of another variable.
    	if(match != null) {
      		for (x in match) {
        		variable = variable.replace(match[x], this.parseVar(globalVars[match[x]]));
      		}
      		return variable;
    	} else {
      		return variable;
		}
	},

	/**
	* FeedbackContainer namespace
	* This is used to store and edit the running feedback variables.
	* Will be used mainly by response objects to update feedback during runtime
	*/
	feedbackContainer : {
		
		//The total amount of response events (for now only keyboard_responses exist)
		totalResp: 0,

		//The total amount of reaction time for every response event
		totalTime: 0,

		//The total amount of correct responses
		totalCorrect: 0,

		/**
		* Increments totalResp. Is used by response objects.
		*/
		incTotalResp: function () {
		    this.totalResp++;
		},

		/**
		* Resets all feedback variables. Will be called by reset_feedback plugin and
		* the feedback item when it is supported.
		*/
		resetFeedback: function () {
		    this.totalResp = 0;
		    this.totalTime = 0;
		    this.totalCorrect = 0;
		    globalVars["[acc]"] = 'NA';
		    globalVars["[avg_rt]"] = 'NA';
		},

		/**
		* Computes average response time
		* If called with 'time', will add that to the total time before computing.
		* @time: the response time that has to be added to totaltime
		* @return: the average response time of the participant
		*/
		getAvgRt: function (time) {
			if(time) {
				this.totalTime += time;
			}
		    return this.totalResp == 0 ? 'NA' : this.totalTime / this.totalResp;
		},

		/**
		* Computes accuracy.
		* If called with 'correct', will increment totalCorrect before computing
		* @correct: if the response was correct or not.
		* @return: the accuracy of the participant
		*/
		getAcc: function (correct) {
			if (correct){
				this.totalCorrect++;
			} 
		    return this.totalResp == 0 ? 'NA' : this.totalCorrect / this.totalResp * 100;
		},
	},

	/**
	* Contains function.
	* Checks whether an item is present in an array
	* @item: the item to be checked for
	* @array: the array to be searched in
	* @return: whether the item has been found or not
	*/
	contains: function (item, array) {
		for (a in array) {
		    if (item == array[a]) {
		        return true;
		    }
		}
		return false;
	},

    /**
    * Function for reading cookie data, taken from Django's documentation page
    * Will be used by utils.postData to extract CSRFtoken that is needed to pass
    * CSRFMiddleware verification on the Django back end.
    * @name: cookievalue to be extracted
    */
    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    /**
    * Used to post 'data' to 'url' with csrfmiddlewaretoken verification
    * Callback function will end the experiment and change page to landing page.
    * @url: the url to be posted to
    * @data: the data to be posted
    */
    postResults: function(url, data) {
         $.post(url, { 
            postdata: data,
            csrfmiddlewaretoken: utils.getCookie('csrftoken')
        }, function(output){
            alert("End of experiment. Thank you for participating.");
            $("body").html(output);
        });
    },

    /**
    * MediaPool namespace
    * This will be used to load and create media pools, so that 
    * bigger files can be preloaded.
    * Supports only imagePool creation as of now
    */
    mediaPool: {

        /**
        * Creates list of JavaScript Image() objects containing every
        * image that is part of the experiment
        * @dir: the directory to be searched in
        * @filenames: filenames used for creating image() objects
        * @return: list of images;
        */
        createImagePool: function(dir, filenames) {
            var pool = [];
            for(file in filenames) {
                obj = new Image();
                obj.src = "../media/" + dir + filenames[file];
                pool[filenames[file]] = obj;
            }
            return pool;
        },
    },
}