/**
* keyboard_response Class
* Represents the keyboard_response from OpenSesame.
* Note that this class does not listen for keypresses itself.
* This is done by the keylistener in utils/keyListener.js
*
* @param name - The name of this object, used to create variables that depend on item name
* @param correctResponse - The correct responses of this class. If left undefined, no response are correct
* @param allowedResponse - The allowed responses. If left undefined, every response is allowed
* @param duration - The duration of this item in ms. Waits for user input if value is 'infinite' 
*/
function keyboard_response (name, correctResponse, allowedResponse, duration) {
	
	//The correct responses for this keyEvent
	//It is a function because correctResponse can be variable and has to be parsed.
	var _correctResponse = function () {
		var string = utils.parseVar(correctResponse);
		//Splitting the string on ';' incase more than one response is correct. In an OS-script this will be semicolon-seperated
		//If correctResponse is undefined (no correctResponse present), every response given by the user will be considered incorrect
		return correctResponse ? string.split(";") : [];
	}

	//The allowed responses for this keyEvent
	//It is a function because allowedResponse can be variable and has to be parsed.
	var _allowedResponse = function () {
		var string = utils.parseVar(allowedResponse);
		//Splitting the string on ';' incase more than one response is correct. In an OS-script this will be semicolon-seperated
		return allowedResponse ? string.split(";") : undefined;
	}

	//The duration this sketchpad should be displayed. 
	//It is a function because duration can be variable and has to be parsed.
	var _duration = function () {
		return duration ? utils.parseVar(duration) : "infinite";
	}

	//The current instantation of this class.
	var me = this;

	//The parent currently calling this object.
	//Objects in opensesame can be reused during runtime, so the parent is not static.
	var parent;

	//Internal timer that is set to go off after _duration has ended, but since a keyboard_response
	//allows transition on keypress or after duration at the same time, we have to have access to the internal
	//timer in order to clear it, in case a key is pressed before the duration time has ended.
	var timer;

	//Timestamp that will be set as soon as this keyboard_response is loaded. Is used to compute reaction time.
	var startTime;

	//Variable that keeps track of how many times this object has been called. It's set to -1 initially.
	var countItem = "[count_" + name + "]";
	globalVars[countItem] = -1;

	//Variable that holds a timestamp of when this object was last called. It's set to "NA" initially.
	var timeItem = "[time_" + name + "]";
	globalVars[timeItem] = "NA";

	//Item specific variable that keeps track of the last pressed key on this keyboard_response.
	//It's set to "NA" initially.
	var responseItem = "[response_" + name + "]";
	globalVars[responseItem] = "NA";

	//Item specific variable that keeps track of the last measured response time on this keyboard_response.
	//It's set to "NA" initially.
	var responseTimeItem = "[response_time_" + name + "]";
	globalVars[responseTimeItem] = "NA";

	//Item specific variable that keeps track of the correctness of the last pressed key on this keyboard_response.
	//It's set to "NA" initially.
	var correctItem = "[correct_" + name + "]";
	globalVars[correctItem] = "NA";
	
	/**
	* Run function.
	* Prepares variables and remains in this state until keyDown() is called by keyListener or until
	* the duration runs out. If duration runs out, variables are set before next object is loaded.
	* @param p - the parent currently calling this run function.
	*/
	this.run = function (p) {
	   	parent = p;
	   	prepare();
		//This will make sure the next slide is loaded by itself (after duration time).
		if(_duration() != "infinite" ) {
			timer = setTimeout(function a () {

				//Set variables
				globalVars[correctItem] = 0;
				globalVars["[correct]"] = 0;
				globalVars[responseTimeItem] = "NA";
				globalVars[responseItem] = "NA";

				//Set the running feedback variables
				globalVars["[acc]"] = utils.feedbackContainer.getAcc(false);
				globalVars["[avg_rt]"] = utils.feedbackContainer.getAvgRt(_duration());
				
				parent.loadNext();
			}, _duration())	
		}
	}

	/**
	* Getter for parent
	* @return - the parent
	*/
	this.getParent = function() {
		return parent;
	}

	/**
	* Preparation function.
	* Will be called by this object's run function.
	* Pepares variables and tells MASTER it's currently being displayed.
	* Increments the total response variable in feedbackContainer.
	* Note: does not need to clear the Canvas, because a keyboard_response doesn't draw anything on it.
	*/
	var prepare = function () {
		globalVars[timeItem] = Date();
		globalVars[countItem]++;
		utils.feedbackContainer.incTotalResp();
		MASTER.setCurrentObject(me);
		startTime = Date.now();
	}

	/**
	* Will be called by keyListener when a key is pressed
	* on this keyboard_response. The timer has to be cleared explicitely
	* to avoid loadNext() being called twice on parent, in case the duration is not 'infinite'.
	* @param key - The pressed character (Will be the actual character, not ascii code)
	* @param time - Timestamp of when the the key was pressed. Used to compute response time
	*/
	this.keyDown = function (key, time) {
		//Check whether the keycode is part of allowedResponses.
		//If no allowedResponses are defined, every response is allowed.
		if (utils.contains(key, _allowedResponse()) || !_allowedResponse()) {
			clearTimeout(timer);

			//Check whether the keycode is a correct response and update variables accordingly.
			if (utils.contains(key, _correctResponse())) {
				globalVars["[acc]"] = utils.feedbackContainer.getAcc(true);
				globalVars[correctItem] = 1;
				globalVars["[correct]"] = 1;
			} else {
				globalVars["[acc]"] = utils.feedbackContainer.getAcc(false);
				globalVars[correctItem] = 0;
				globalVars["[correct]"] = 0;
			}

			//Set variables.
			var respTime = time - startTime;
			globalVars[responseItem] = key;
			globalVars[responseTimeItem] = respTime;
			globalVars["[response]"] = key;
			globalVars["[response_time]"] =  respTime;

			//Set the running feedback variables.
			globalVars["[avg_rt]"] = utils.feedbackContainer.getAvgRt(respTime);

			//Finally, load the next object.
			parent.loadNext();
		}
	}
}