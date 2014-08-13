/**
* Fixdot object class
* This class represents a draw fixdot statement that is used in sketchpads to draw a fixdot on the screen
*
* @param x - coordinate on x-axis of this item
* @param y - coordinate on y-axis of this item
* @param color - the color of this fixdot
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function fixdot(x, y, color, condition) {
	
	//x coord on the canvas of this image object.
	var _x = parseFloat(x);

	//y coord on the canvas of this image object.
	var _y = parseFloat(y);

	//The color of this fixdot
	var _color = color;

	//Draw condition. Only if the condition holds, the object will be drawn on screen
	//Has to be parsed first, because this can contain variable names
	var _condition = function () {
		return utils.parseVar(condition);
	}
	
	/**
	* Draw function.
	* Will be called by the sketchpad this fixdot item belongs to. 
	* It draws a filled circle with a radius that is dependent on the experiment width.
	*/
	this.draw = function () {
		if(eval(_condition())) {
			var fixdot = new fabric.Circle({
			 	radius: screen.width/120, 
			 	fill: _color, 
			});
			fixdot.set({
				left: _x + CANVAS.getWidth() / 2 - fixdot.getWidth() / 2, 
				top: _y + CANVAS.getHeight() / 2 - fixdot.getHeight() / 2
			});
			CANVAS.add(fixdot);
		}
	}
}