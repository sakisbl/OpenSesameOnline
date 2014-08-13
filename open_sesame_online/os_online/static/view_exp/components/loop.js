/**
* loop class
* Represents the loop item in OpenSesame
* Runs an item repeatedly
*
* @param name - The name of this object, used to create variables that depend on item name
* @param repeat - The amount of times a cycle should be repeated. 1 by default
* @param skip - The amount of cycles that have to be skipped at the start of the loop. 0 by default
* @param offset - Denotes whether or not this loop has to run in offset mode. No by default
* @param item - The item that this loop item repeatedly runs
* @param breakIf - Breakcondition of this loop item. False by default
* @param columnOrder - List of strings that denotes the order of the variables that this loop item creates. 
* @param cycles - The amount of cycles this loop runs. 1 by default
* @param order - The order in which this loop item has to run through cycles. Random by default
* @param cyclelist - List of cycles that represents the setcycle statements that belong to the loop.
*/
function loop(name, repeat, skip, offset, item, breakIf, columnOrder, cycles, order, cycleList) {

	//The amount of repeats of this loop
	//It is a function because repeat can be variable and has to be parsed.
	var _repeat = function () {
		return repeat ? utils.parseVar(repeat) : 1;
	}

	//The amount of cycles of this loop
	//It is a function because cycles can be variable and has to be parsed.
	var _cycles = function () {
		return cycles ? utils.parseVar(cycles) : 1;
	}

	//The break_if statement of this loop
	//It is a function because break_if can be variable/contains variablenames and has to be parsed.
	var _breakIf = function () {
		return breakIf ? utils.parseVar(breakIf) : false;
	}

	//The number of cycles that have to be skipped at the start of the loop
	var _skip = skip || 0;

	//Indicates whether skipped cycles should be displayed after loop or not
	var _offset = offset || "no";

	//Indicates the order in which cycles have to be played.
	var _order = order || "random";

	//An array that represents the columnorder of this loop
	var _columnOrder = columnOrder;

	//This internal counter is used to keep track of how many times a cycle has been repeated.
	var repCounter = 0;

	//This internal counter is used to keep track of many cycles have been played
	//Is initialized with value of _skip so that the loop will start off at the correct cycle
	//in case something has to be skipped.
	var cycleCounter = _skip;

	//The item that this loop repeatedly calls
	var _item = item;

	//The cyclelist that represents all setcycle statements. This list is created by the translator
	//and will be shuffled in case the order is 'random'
	var _cycleList = cycleList ? (_order == "random" ? utils.shuffle(cycleList) : cycleList) : [];

	//Indicates whether or not this loop has to run in offsetMode or normalMode
	var offsetReached = false;

	//Initialize all variables in this loop with "NA"
	for (i in _columnOrder) {
		globalVars[_columnOrder[i]] = "NA";
	}

	//The current instantation of this class.
	var me = this;

	//The parent currently calling this object.
	//Objects in opensesame can be reused during runtime, so the parent is not static.
	var parent;

	//Variable that keeps track of how many times this object has been called. It's set to -1 initially.
	var countItem = "[count_" + name + "]";
	globalVars[countItem] = -1;

	//Variable that holds a timestamp of when this object was last called. It's set to "NA" initially.
	var timeItem = "[time_" + name + "]";
	globalVars[timeItem] = "NA";

	/**
	* Run function.
	* Calls prepare and loads the first cycle.
	* @param p - the parent currently calling this run function
	*/
	this.run = function (p) {
		parent = p;		
		prepare();
		//Nothing has to be done if this loop starts off at a cycle number higher than cycleCounter
		//or if the breakcondition is already met.
		if(_cycles() > cycleCounter && !eval(_breakIf())){
			setcycle();
			_item.run(me);
		} else {
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
	* Prepares this loop item for offsetMode. In offsetMode, we cycle through every item
	* that was skipped at the start and set variables accordingly. 
	* Will be called from normalMode when it has ended and this loop item requires offsetMode.
	*/
	var initOffset = function () {
		cycleCounter = 0;
		offsetReached = true;
		setcycle();
		item.run(me);
	}

	/**
	* Normal loopMode of this loop item. Will cycle through cyclelist until it has reached the end of _cycles()
	* If _offset is turned on, it initializes offsetMode at the end of normalMode.
	* Calls loadNext() on parent if the end of normalMode has ended and _offset == "no".
	*/
	var normalMode = function () {
		if (cycleCounter < _cycles()) {
			setcycle();
			_item.run(me);
		} else if (_offset == "yes") {
			initOffset();
		} else {
                        resetState();
			parent.loadNext();
		}
	}

	/**
	* OffsetMode of this loopitem. In this mode, the loop will run from cyclecounter until _skip (_skip denotes the amount of skipped cycles)
	* Calls loadNext() on parent if the end of offsetMode has been reached.
	*/
	var offsetMode = function () {
		if (cycleCounter < _skip) {
			setcycle();
			_item.run(me);
		} else {
                        resetState();
			parent.loadNext();
		}
	}

	/**
	* Loads the next cycle of this loop and calls next on parent
	* if this loop has come to an end. Will be called by the item that
	* this loop repeatedly runs.
	*/
	this.loadNext = function () {
		repCounter++;

		//We may only update cycleCounter if we've had the required number of repetitions
		if(repCounter == _repeat()) { 
			cycleCounter++;
			repCounter = 0;
		}

		//A loop can run in either offsetMode or normalMode. This depends on offsetReached.
		//offsetReached will be set at the end of normalMode and _offset == "yes".
		//If the breakcondition is met, this loop ends right away and loadNext() is called on parent.
		if (!eval(_breakIf())) {
			if (offsetReached) {
				offsetMode();
			} else {
				normalMode();
			}
		} else {
                        resetState();
			parent.loadNext();
		}
	}

	/**
	* Sets the variables this loop defines to the value that corresponds with the
	* current cycle. 
	*/
	var setcycle = function () {
		if(_cycleList) {
			for (i in _columnOrder) {
				globalVars[columnOrder[i]] = cycleList[cycleCounter][_columnOrder[i]];
			}			
		}
	}

	/**
	* Getter for the item that this loop runs
	* @return - item that this loop runs
	*/
	this.getItem = function () {
		return _item;
	}

	/**
	* Resets state of this loop in case it's
	* reused somewhere else in the experiment.
	*/
    var resetState = function () {
            cycleCounter = _skip;
            repCounter = 0;
    }

    /**
    * Getter for parent
    * @return - the parent
    */
    this.getParent = function() {
		return parent;
	}
}