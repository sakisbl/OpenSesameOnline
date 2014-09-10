/**
* sequence class
* This represents a sequence in which objects are run.
*
* @param name - The name of this object, used to create variables that depend on item name
* @param objects - List of objects this sequence runs
* @param conditions - List of runconditions that correspond with the objects
*/
function sequence(name, objects, conditions) {
	
	//Array of objects this sequence consists of.
	var _objects = objects;

	//Array of conditions that belong to an object in the objects array
	var _conditions = conditions;

	//Counter that is used to select items from the objects array and belonging conditions from the conditions array.
	var objectCounter = 0;

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
	* Sets parent and runs the first object if the condition holds
	* @param p - the parent this run function was called from.
	*/
	this.run = function (p) {
		parent = p;
		prepare();
        //First, check if there is any object to be run
		if(_objects[objectCounter]) {
			//If there is, check if the corresponding condition holds
			if (eval(utils.parseVar(_conditions[objectCounter]))) {
				_objects[objectCounter].run(me);
			} else {
				this.loadNext();
			}
		} else {
			//We can call loadNext() on parent immediately when this sequence doesn't contain objects
            resetState();
			parent.loadNext();
		}
	}

	/**
	* Preparation function.
	* Will be called by this object's run function.
	* Pepares variables and tells MASTER it's currently being displayed.
	*/
	var prepare = function () {
		MASTER.setCurrentObject(me);
		globalVars[timeItem] = Date();
		globalVars[countItem]++;
	}

	/**
	* loadNext function.
	* This function is used to play through the objects opensesame consists of.
	*/
	this.loadNext = function () {
		objectCounter++;
		if(objectCounter == _objects.length) {	
			//Sequence has now ended, call next on parent so it knows it can proceed
			resetState();
			parent.loadNext(); 
		} else if (objectCounter < _objects.length){
			//Sequence is still running, so we evaluate the condition of the next object
			if (eval(utils.parseVar(_conditions[objectCounter]))) {
		   		//And run it in case of success.
		   		_objects[objectCounter].run(me);
			} else {
				//Skip it in case of failure.
				this.loadNext();
			}
		}
	}

	/**
	* Resets state of this sequence in case it's
	* reused somewhere else in the experiment.
	*/
    var resetState = function () {
        objectCounter = 0;
    }

    /**
    * Getter for parent
    * @return - the parent
    */
    this.getParent = function() {
		return parent;
	}

	/**
	* Getter for objectCounter
	* @return - objectCounter
	*/
    this.getObjectCounter = function() {
    	return objectCounter;
    }

    /**
    * Getter for _objects
    * @return - _objects
    */
    this.getObjects = function() {
    	return _objects;
    }
}