/**
* Experiment class
* This represents the top of the hierarchy in which the objects of an
* experiment are ordered. There can only be one of these per experiment.
* The object of this class has to be a sequence.
* @param object - The top sequence (entry point) of this experiment.
*/
function Experiment (object) {
	
	//The object that starts the entire experiment
	var object = object;

	//Value that represents if the experiment has ended or not. 0 means not ended and 1 means ended.
	var experimentEnded = 0;

	//The current instantiation of this class. This is used to tell other functions this instantiation is their parent.
	var me = this;

	//The object that's currently being displayed on the screen. Every object that runs, no matter how deep into the hierarchy
	//of the experiment, will report to this MASTER experiment class to tell it's currently being displayed on screen
	var currentObject;

	//This represents the list of loggers this experiment consists of. Loggers are added to the master experiment to easily
	//collect and prepare all logged data after the experiment has finished. Currently, the Django back end has support for one logger item per experiment
	var loggers = [];

	/**
	* Readies a data object to be posted to the back end by merging all logger items together
	* Because the Django backend currently only has support for one logger item, nothing has to be merged
	* and only the first element of loggers will be returned
	*/
	var prepareLogs = function () {
		//Pushing an empty object into loggers in case loggers has not been filled yet.
		//This means setLog() was never called and so there is no logger item running in this experiment
		if (loggers.length <= 0) {
			return JSON.stringify({});
		}
		//Returning JSON stringified object of the first logger in the list. Only the first one,
		//since Django back end does not support multiple loggers.
		return JSON.stringify(loggers[0].getOutput());
	}

	/**
	* Run function.
	* Prepares canvas for first use and 
	* calls run on object and starts off the experiment if object is a sequence.
	*/
	this.run = function () {
		if(!(object instanceof sequence)) {
			alert("Not instantiated with a sequence, ending experiment.");
			return;
		} else {
			utils.canvasPrepare(globalVars["background"]);
    		object.run(me);
		}
	}

	/**
	* If this is called by an object, it means the sequence this class started in the run function
	* has now ended and so the entire experiment is over. Will call prepareLogs to send results to the back end
	*/
	this.loadNext = function () {
		experimentEnded = 1;
		utils.postResults("", prepareLogs());
	}

	/**
	* Tells the master experiment (this class) that an object is currently being run.
	* Because results are POSTed to the backend, only once when the entire experiment has ended
	* there is a risk that a user closes the experiment as soon as he reaches the 'goodbye' item
	* When the last object has not been finished, the experiment never ended and so results are never POSTed
	* To prevent this, a check isLast is built that will end the experiment by automatically calling loadNext()
	* (This solution is not ideal and was still in development)
	* @param object - the object to be set
	*/
	this.setCurrentObject = function (object) {
		if(utils.isLast(object)) {
			this.loadNext();
		} else {
			currentObject = object;	
		}
	}

	/**
	* Generally used by KeyListener, which runs globally and will 
	* need acces to the currentObject in the experiment.
	* @return - currentObject
	*/
	this.getCurrentObject = function () {
		return currentObject;
	}

	/**
	* Also used by KeyListener to find out whether it still has to listen
	* for input or not.
	* @return - experimentEnded
	*/
	this.getExperimentEnded = function () {
		return experimentEnded;
	}

	/**
	* Used by logger items to include themselves to the list of loggers
	* @param logger - the logger to be set
	*/
	this.setLog = function (logger) {
		loggers.push(logger);
	}
}