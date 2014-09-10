/**
* Reset_feedback class
* Small plugin that can reset running feedback variables
*
* @param name - The name of this object, used to create variables that depend on item name
*/
function reset_feedback (name) {

	//The parent currently calling this object.
	//Objects in opensesame can be reused during runtime, so the parent is not static.
	var parent;

	//Variable that keeps track of how many times this object has been called. It's set to -1 initially.
	var countItem = "[count_" + name + "]";
	globalVars[countItem] = -1;

	//Variable that holds a timestamp of when this object was last called.
	var timeItem = "[time_" + name + "]";
	globalVars[timeItem] = "NA";

	//The current instantation of this class.
	var me = this;

	/**
	* Run function.
	* Resets the feedback variables and immediately loads next object
	* @param p - the parent currently calling this run function.
	*/
	this.run =  function (p) {
		parent = p;
		prepare();
		utils.feedbackContainer.resetFeedback();
		p.loadNext();
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
	* Sets variables and tells MASTER it's currently being run.
	*/
	var prepare = function () {
		MASTER.setCurrentObject(me);
		globalVars[timeItem] = Date();
		globalVars[countItem]++;
	}
}