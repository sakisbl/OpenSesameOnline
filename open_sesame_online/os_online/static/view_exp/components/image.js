/**
* Image object class
* This class represents an image statement that is used in sketchpads to draw an image on the screen
*
* @param x - coordinate on x-axis of this item
* @param y - coordinate on y-axis of this item
* @param source - the imagename
* @param scale - the scaling of this image
* @param center - denotes whether coordinates should be computed from center of image or topleft corner
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function img(x, y, source, scale, center, condition) {
	
	//x coord on the canvas of this image object.
	var _x = parseFloat(x);

	//y coord on the canvas of this image object.
	var _y = parseFloat(y);

	//scale of this image object.
	var _scale = scale;

	//Source path from which the image has to be loaded.
	//It is a function because source can be variable and has to be parsed.
	var _source = function () {
		return utils.parseVar(source);
	}

	//Variable that says if coordinates have to be computed from the center of the image
	//or from the top left corner.
	var _center = center;

	//Draw condition. Only if the condition holds, the object will be drawn on screen
	//Has to be parsed first, because this can contain variable names
	var _condition = function () {
		return utils.parseVar(condition);
	}
	
	/**
	* Draw function.
	* Will be called by the sketchpad this img item belongs to. 
	* Uses Fabric's image-method to create and manipulate an image selected from the IMAGEPOOL
	*/
	this.draw = function () {
		s = IMAGEPOOL[_source()];
		if(eval(_condition)) {
			oImg = new fabric.Image(s);
			oImg.scale(_scale);
			if(_center == 0) {
				oImg.setLeft(_x + CANVAS.getWidth() / 2);
				oImg.setTop(_y + CANVAS.getHeight() / 2);
			} else {
				oImg.setLeft(_x + CANVAS.getWidth() / 2 - oImg.getWidth() / 2);
				oImg.setTop(_y + CANVAS.getHeight() / 2 - oImg.getHeight() / 2);
			}
			CANVAS.add(oImg);
		}
	}
}