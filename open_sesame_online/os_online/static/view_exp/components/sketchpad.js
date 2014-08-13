/**
* sketchpad Class
* Represents sketchpad item in OpenSesame
* 
* @param name - The name of this object, used to create variables that depend on item name
* @param duration - The duration of this item in ms. Waits for user input if value is 'keypress'
* @param objects - List of objects that this sketchpad item has to draw
*/
function sketchpad(name, duration, objects) {

	//The objects that are to be drawn on the sketchpad (images, textlines, shapes).
	var _objects = objects || [];

	//The duration this sketchpad should be displayed. 
	//It is a function because duration can be variable and has to be parsed.
	var _duration = function () {
		return duration ? utils.parseVar(duration) : "keypress";
	}

	//The current instantation of this class.
	var me = this;

	//The parent currently calling this object.
	//Objects in opensesame can be reused during runtime, so the parent is not static.
	var parent;

	//Variable that keeps track of how many times this object has been called. It's set to -1 initially.
	var countItem = "[count_" + name + "]";
	globalVars[countItem] = -1;

	//Variable that holds a timestamp of when this object was last called.
	var timeItem = "[time_" + name + "]";
	globalVars[timeItem] = "NA";
	
	/**
	* Run function
	* Will be called by a parent (sequence or loop)
	* Prepares variables and draws every object from the _objects array onto the canvas
	* @param p - the parent currently calling this run function.
	*/
	this.run = function (p) {
		parent = p;
		prepare();
		for(var i = 0; i < objects.length; i++) {
			_objects[i].draw();
		}

		//This will make sure the next slide is loaded by itself (after duration time).
		if(_duration() != "keypress" ) {
			setTimeout(function a () {
				parent.loadNext();
			}, _duration())	
		}
	}

	/**
	* Preparation function.
	* Will be called by this object's run function.
	* Pepares variables, clears the CANVAS to remove previously drawn objects 
	* and tells MASTER it's currently being displayed.
	*/
	var prepare = function () {
		MASTER.setCurrentObject(me);
		globalVars[timeItem] = Date();
		globalVars[countItem]++;
		utils.canvasPrepare(globalVars["background"]);
	}

	/**
	* Getter for _duration.
	* Will be called by keyListener to figure out if
	* it has to act or not. In case of the duration being 'keypress',
	* the keylistener will call loadNext() on this object.
	* @return - duration of this object.
	*/
	this.getDuration = function () {
		return _duration();
	}

	/**
	* Getter for parent
	* @return - current parent of this object.
	*/
	this.getParent = function () {
		return parent;
	}

	/**
	* Will be called by keyListener when a key is pressed on this sketchpad.
	*/
	this.keyDown = function (key, time) {
		parent.loadNext();
	}
}