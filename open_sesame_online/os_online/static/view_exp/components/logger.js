/**
* logger Class
* Will always surround with quotes, due to back end data structures
* Does not support igoring missing values. Does always log all variables, regardless of value.

* @param name - The name of this object, used to create variables that depend on item name
* @param variables - A list of variable names that have to be logged. If left undefined, all variables will be logged
*/
function logger (name, variables) {
	
	//The variables that the user wants to log explicitely.
	//This will be a list of variable names in case the Opensesame script file contains log "varname" statements
	//If there are none, _variables will be undefined.
	var _variables = variables;

	/**
	* This is the initial output object that will contain all logged data.
	* On every call of this logger item, the appropriate variables from the globalVars array will be pushed into this object.
	* This object will be turned into JSON with JSON.stringify(output) and posted to the Python backend where it will be turned into a table.
	* 
	* Example of a JSON string and its corresponding table: 
	* 
	* output = {"[response_key1]":["65","66","65","66","65"],"[response_key2]":["32","32","32","32","32"]}
	*
 	* Table:
	* [response_key1]	[response_key2]
	*	65			           32
	*	66			           32
	*	65			           32
	*	66			           32
	*	65			           32
	*/
	var output = {};

	//Variable that says whether this logger item is run for the first time or not.
	var firstTime = 1;

	//The current instantation of this class.
	var me = this;

	//Variable that keeps track of how many times this object has been called. It's set to -1 initially.
	var countItem = "[count_" + name + "]";
	globalVars[countItem] = -1;

	//Variable that holds a timestamp of when this object was last called.
	var timeItem = "[time_" + name + "]";
	globalVars[timeItem] = "NA";

	//The parent currently calling this object.
	//Objects in opensesame can be reused during runtime, so the parent is not static.
	var parent;

	/**
	* Function that initializes the fields of the output object and sets item specific variables.
	*/
	var prepare =  function () {
		
		//Initiliazes output object incase this is the first time this logger item is called.
		if (firstTime == 1) {
			logInit();
			firstTime = 0;
		}
		MASTER.setCurrentObject(me);
		globalVars[timeItem] = Date();
		globalVars[countItem]++;
	}
	
	
	/**
	* Logger initialize function.
	* Before being able to push variable values into the output object, we have to initialize the correct fields with an empty array.
	* This only has to be done once (the first time this logger is called).
	* After this intialization, lines with variable values will be pushed into the empty arrays on every call of this item (this is done by the run function)	
	*/
	var logInit = function () {
		
		//If _variables is not undefined, we only have to create the fieldnames that are in _variables.
		//Otherwise, a field will be created for all variables in globalVars.		
		if(_variables) {
			for (a in _variables) {
				output[_variables[a]] = [];
			}
		} else {
			for (a in globalVars) {
				output[a] = [];
			}
		}
		//Adding this logger to the logpool in MASTER experiment.
		MASTER.setLog(me);
	}
	
	/**
	* Run function
	* Calls prepare and the appropriate log function before calling next on parent.
	* @param p - the parent currently calling this run function.
	*/
	this.run = function (p) {
		parent = p;
		prepare();
		log(_variables);
		p.loadNext();
	}
	
	/**
	* Logging function that builds the output object of this class
	* Logs all in globalVars, unless a varlist is passed to this function.
	* Then only the variables in varlist will be logged.
	* @param varlist - the variables the user wants to log.
	*/	
	var log =  function (varlist) {
		if(varlist) {
			for (a in varlist) {
				eval("output['"+ variables[a] +"'].push('" + globalVars[variables[a]] +"')");
			}
		} else {
			for (a in globalVars) {
				eval("output['"+ a +"'].push('" + globalVars[a] +"')");
			}
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
	* Getter for the output object
	* @return - the output object of this logger class.
	*/
	this.getOutput = function () {
		return output;
	}
}