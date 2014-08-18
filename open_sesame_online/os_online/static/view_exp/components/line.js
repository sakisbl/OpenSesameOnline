/**
* Draw line object class
* This class represents a draw line statement that is used in sketchpads to draw a line on the screen
*
* @param left - the left-most x-coordinate
* @param right - the right-most x-coordinate
* @param top - the top y-coordinate
* @param bottom - the bottom y-coordinate
* @param penwidth - line thickness
* @param color - the color of this fixdot
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function line(left, top, right, bottom, penwidth, color, condition) {
    
    //left coord on the canvas of this image object.
    var _left = parseFloat(left);

    //right coord on the canvas of this image object.
    var _right = parseFloat(right);

    //top coord on the canvas of this image object.
    var _top = parseFloat(top);

    //bottom coord on the canvas of this image object.
    var _bottom = parseFloat(bottom);

    //width of line
    var _penwidth = parseFloat(penwidth);

    //The color of this line
    var _color = color;

    //Draw condition. Only if the condition holds, the object will be drawn on screen
    //Has to be parsed first, because this can contain variable names
    var _condition = function () {
        return utils.parseVar(condition);
    }
    
    /**
    * Draw function.
    * Will be called by the sketchpad this line item belongs to. 
    * It draws a line.
    */
    this.draw = function () {
        if(eval(_condition())) {
            var line = new fabric.Line([_left + CANVAS.getWidth()/2, _top + CANVAS.getHeight()/2, _right + CANVAS.getWidth()/2, _bottom + CANVAS.getHeight()/2], {
                stroke: _color,
                strokeWidth: _penwidth,
            });
            CANVAS.add(line);
        }
    }
}