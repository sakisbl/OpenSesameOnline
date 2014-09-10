/**
* text_display Class
* Represents text_display item in OpenSesame
*
* @param name - The name of this object, used to create variables that depend on item name
* @param foreground - The text color
* @param fontSize - Size of the text
* @param align - Alignment of text
* @param content - The text to be put on screen
* @param background - The background color that has to be shown when this textdisplay plays
* @param fontFamily - The fontFamily
*/
function text_display (name, foreground, fontSize, align, content, background, duration, fontFamily) {

	//Textcolor. It is a function because the color can be variable and has to be parsed.
	var _foreground = function () {
		return foreground ? utils.parseVar(foreground) : "white";
	}

	//Fontsize. 18 by default.
	var _fontSize = fontSize || 18;

	//Text alignment. Center by default
	var _align = align || "center";

	//The Fabric text element that will be drawn on the canvas.
	//It is a function because the content can be variable and has to be parsed.
	var text =  function () {
		return new fabric.Text(utils.parseVar(content));
	}

	//Background color. It is a function because the color can be variable and has to be parsed.
	var _background = function () {
		return background ? utils.parseVar(background) : "black";
	}

	//The duration this sketchpad should be displayed. 
	//It is a function because duration can be variable and has to be parsed.
	var _duration = function () {
		return duration ? utils.parseVar(duration) : "keypress";
	}

	//Fontfamly. mono by default.
	var _fontFamily = fontFamily || "mono";

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
	* Run function.
	* Will be called by a parent (sequence or loop)
	* Prepares variables and draws the text object on the canvas
	* @param p - the parent currently calling this text_display.
	*/
	this.run = function  (p) {
		parent = p;
		prepare();
		placeText();
		//This will make sure the next slide is loaded by itself (after duration time)
		if(_duration() != "keypress" ) {
			setTimeout(function a () {
				parent.loadNext();
			}, _duration())			
		}
	}

	/**
	* Prepares fabric text element, manipulates it depending on the attributes and adds it
	* to the Canvas. The objec is always placed in the center
	*/
	var placeText = function () {
		var t = text();
		t.set({
				fill: _foreground(),
				fontFamily: _fontFamily,
				fontSize: _fontSize,
				textAlign: align,
		});
		utils.alignCenter(t);
		CANVAS.add(t);
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
		utils.canvasPrepare(_background());
	}

	/**
	* Getter for _duration.
	* Will be called by keyListener to figure out if .
	* it has to act or not. In case of the duration being 'keypress',
	* the keylistener will call loadNext() on this object.
	* @return: duration of this object.
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
	* Will be called by keyListener when a key is pressed on this textdisplay.
	*/
	this.keyDown = function (key, time) {
		parent.loadNext();
	}
}