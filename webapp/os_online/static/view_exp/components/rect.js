/**
* Rectangle object class
* This class represents a draw rectangle statement that is used in sketchpads to draw a rectangle on the screen
*
* @param x - the left x coordinate
* @param y - the top y coordinate
* @param w - the width
* @param h - the height
* @param fill - a boolean indicating whether the rectangle is outlined (false) or filled (true)
* @param penwidth - line thickness
* @param color - the color of this rectangle
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function rect(x, y, w, h, fill, penwidth, color, condition) {
    
    //x coord on the canvas of this object.
    var _x = parseFloat(x);

    //y coord on the canvas of this object.
    var _y = parseFloat(y);

    //the width of this object
    var _w = parseFloat(w)

    //the height of this object
    var _h = parseFloat(h)

    //the fill boolean indicating whether the rectangle is outlined or filled
    var _fill = parseFloat(fill)

    //width of line
    var _penwidth = parseFloat(penwidth);

    //The color of this circle
    var _color = color;

    //Draw condition. Only if the condition holds, the object will be drawn on screen
    //Has to be parsed first, because this can contain variable names
    var _condition = function () {
        return utils.parseVar(condition);
    }
    
    /**
    * Draw function.
    * Will be called by the sketchpad this rectangle item belongs to. 
    * It draws a rectangle.
    */
    this.draw = function () {
        if(eval(_condition())) {
            if(fill == 0){
                var rectangle = new fabric.Rect({
                    left: _x + CANVAS.getWidth()/2,
                    top: _y + CANVAS.getHeight()/2,
                    width: _w,
                    height: _h,
                    stroke: _color,
                    strokeWidth: _penwidth,
                  });
                CANVAS.add(rectangle);
            } else {
                var rectangle = new fabric.Rect({
                    left: _x + CANVAS.getWidth()/2,
                    top: _y + CANVAS.getHeight()/2,
                    width: _w,
                    height: _h,
                    fill: _color,
                  });
                CANVAS.add(rectangle);
            }
        }
    }
}