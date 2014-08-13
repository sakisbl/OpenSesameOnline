# OpenSesame JavaScript Engine: *Quick overview*

This is a more global overview of how the OpenSesame engine works in JavaScript. For a more in-depth and low level explanation of code, it is advised to look at the documentation that is written in the code.


## Items
As of now the following items have been implemented:

* Sequence
* Loop
* Text display
* Keyboard response
* Sketchpad (with support for only textline, image and fixdot)
* Logger (Backend supports only one logger per experiment as of now)
* Reset feedback plugin

You can find all static files that belong to this part of the webapp in the following directory: open_sesame_online/os_online/static/view_exp/

The translated scriptfile that is served to the user is in the directory:
open_sesame_online/os_online/media/"experiment name"
"experiment name" is a unique name that is generated randomly.

The actual HTML page that is shown to the user can be found here:
open_sesame_online/os_online/view_exp/templates/show.html


## How does it begin
When the script is translated by the translator in the backend, a JavaScript file comes out that is similar to the OpenSesame script. For every define block, there will be a line of JS (JavaScript) code that creates a new instance of a function that belongs to the item being defined by the OS (OpenSesame) scriptfile. 

At the very end of the translated script, an object called MASTER is created. This object holds the entry point of the experiment. The entry point is the first sequence that’s present in every experiment. From this first sequence, all other objects are run. 

Below, an explanation will be given on the general structure and flow of data in experiments in the JS-engine.


## Sequences
A sequence in the JS-engine is a function that holds a list of objects and a list of conditions. The first time this sequence is called, it will call the run-function that belongs to the first object that this sequence holds (if the run-condition holds). As soon as the object has finished running, it will report back to the sequence it was called from (by calling its loadNext-function), so it knows it can proceed. The object counter is incremented and now the next object in the sequence is called. 

When the sequence has run its last item, it will call a loadNext function on its parent. If this parent happens to be the MASTER experiment, then it means the entry point sequence has ended, so the entire experiment is over. In case this sequence was inside another sequence, the next sequence is started and the experiment continues. This is how the JS-engine runs through all the items in the experiment.


## Loops
Just like sequences, loops can manipulate the structure and order of the experiment. When a loop item is called for the first time, it will call the run-function of the object it is supposed to run. When that object has finished running, it will report back to this loop. This means one cycle has been completed. All variables are set according to the new cycle before the run-function is called again. When all cycles have been completed, this loop reports to its parent as well and the next item from the sequence this loop is in will be run.


## User input handling
When a user presses a key, the keylistener in keyListener.js will go off and determine if this keypress should be handled or ignored. In case it has to be handled, it will call the keydown function of the object that’s currently being displayed/run. As of now, not all keys that are allowed in OpenSesame are mapped to what is allowed in JavaScript. For example 'slash' is a valid key in OpenSesame, but in JavaScript, it has to be mapped to '/'. 


## globalVars
The JS-engine deals with two types of variables: user defined variables (in loops) and default variables (accuracy, response times etc.). All of these will be saved and altered in a global dictionary, called globalVars. When an item is called and it has to load a variable, it will call the parseVar function in utilities.js. This will look at the current value that belongs to that variable name in globalVars and returns it. 


## Extending the current framework
If you would like to create a new item, it needs to have at least a run-function implemented, with one parameter: the parent. Because objects can be reused during runtime, the parent of an object can change, so it has to be passed on to its run-function, in order to be able to call the loadNext-function on the correct parent. In case this object can manipulate the canvas, you have to call the prepare canvas function from utilities.js.  This function will clear and prepare the canvas for this item.

In case you’re implementing a new draw-type of the sketchpad, for example lines or other shapes, this object won’t need a run-function. Instead, it needs a draw-function. A sketchpad will have a list of draw-types and when the sketchpad is run, it will call the draw-function on ever draw-type in that list. Because draw items don’t need a run-function, they also don’t have to be able to call loadNext on their parent. This is handled by the sketchpad itself.


## The media pool
In utilities.js you will find a media pool namespace. As of now, the only media files this engine supports, are image files. When the user plays the experiment, all image files are returned by a function in the python backend that lists all filenames in a directory with a certain file extension (.jpg, .png in this case). These filenames are parsed and made into a list that is usable in JavaScript, called IMAGEPOOL (IMAGEPOOL is located in open_sesame_online/os_online/view_exp/templates/show.html). Everytime an image is created in image.js, the already loaded image object will be taken from the IMAGEPOOL.

In case you want to add other types of files to the pool, you have to go into open_sesame_online/os_online/view_exp/views.py and change the function view_experiment that uses get_dir to retrieve filenames.

## Logging results
Results will be logged by the logger item. When the experiment is running and a logger item is called, it will record the variables it was assigned to record. It will never ignore missing (since this was also not recommended on the official OpenSesame website) and always surround with quotes, because this is easier for the backend, where every result will be stored into a database. As soon as the experiment ends, the entire logger item is turned into JSON and sent to the backend where it will be parsed.

The backend does not support multiple loggers as of now, however when designing logger functionality in this JS-engine, we kept in mind that in the future multiple loggers may be supported. Preparing the loggers before posting data is done in Experiment.js.

An issue we ran into is that if the user reaches the last 'goodbye' item, he might think that the experiment has ended and closes his browser instead of pressing the last key to post his data. As a result, no data of this experiment was saved and the user has to do it again. To prevent this from happening, we implemented a check that will automatically play through the last item by itself, so that the experiment ends properly and data is saved.

However, this check is rather naive and incomplete as of now. It assumes that the last item in the entry point sequence will not be a loop or a sequence itself. If it does end with one of these, the check will not be able to detect this, and the last item will not be automatically played, so the user runs the risk of exiting the experiment too early.