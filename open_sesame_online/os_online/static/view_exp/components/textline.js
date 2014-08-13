/**
* Textline object class
* This class represents a textline statement that is used in sketchpads to draw a line of text on the screen
* HTML tag parsing is not supported, so tags will appear as plain text.
*
* @param x - coordinate on x-axis of this item
* @param y - coordinate on y-axis of this item
* @param content - the text to be drawn
* @param center - denotes whether coordinates should be computed from center of image or topleft corner
* @param color - text color
* @param fontFamily - The fontFamily
* @param fontSize - Size of the text
* @param fontItalic - denotes whether text should be italic or not
* @param fontBold - denotes whether text should be bold or not
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function textline(x, y, content, center, color, fontFamily, fontSize, fontItalic, fontBold, condition) {
	
	//x coord on the canvas of this image object.
	var _x = parseFloat(x);

	//y coord on the canvas of this image object.
	var _y = parseFloat(y);

	var _content = function () {
		return utils.parseVar(content);
	}

	//Variable that says if coordinates have to be computed from the center of the image
	//or from the top left corner.
	var _center = center;

	//Specifies text color
	var _color = color;

	//Specifies font family. If font family is unknown, default will be loaded by browser
	var _fontFamily = fontFamily;

	//Specifies font size
	var _fontSize = fontSize;

	//Specifies font style
	var _fontItalic = fontItalic

	//Specifies font weight
	var _fontBold = fontBold;

	//Draw condition. Only if the condition holds, the object will be drawn on screen
	//Has to be parsed first, because this can contain variable names
	var _condition = function () {
		return utils.parseVar(condition);
	}
	
	/**
	* Draw function.
	* Will be called by the sketchpad this img item belongs to. 
	* Uses Fabric's text function to render and position text on screen.
	*/
	this.draw = function () {
		if(eval(_condition())) {
			t = _content();
			var text = new fabric.Text(t);

			//Set styling of the text
			text.set({
				fill: _color,
				fontFamily: _fontFamily,
				fontSize: _fontSize,
				fontStyle: _fontItalic == "yes" ? 'italic' : 'normal',
				fontWeight: _fontBold == "yes" ? 'bold' : 'normal',
				left: _x + CANVAS.getWidth() / 2,
				top:  _y + CANVAS.getHeight() / 2,
				textAlign: 'center'
			});
			if(center == 1) {
				text.set({
					left: _x + CANVAS.getWidth() / 2 - text.getWidth() / 2,
					top:  _y + CANVAS.getHeight() / 2 - text.getHeight() / 2
				})
			}
			CANVAS.add(text);
		}
	}
}