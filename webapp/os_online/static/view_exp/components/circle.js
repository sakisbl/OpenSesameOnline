/**
* Circle object class
* This class represents a draw circle statement that is used in sketchpads to draw a circle on the screen
*
* @param x - coordinate on x-axis of this item
* @param y - coordinate on y-axis of this item
* @param radius - the radius length of the circle
* @param fill - a boolean indicating whether the cirles is outlined (false) or filled (true)
* @param penwidth - line thickness
* @param color - the color of this circle
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function circle(x, y, radius, fill, penwidth, color, condition) {
    
    //x coord on the canvas of this object.
    var _x = parseFloat(x);

    //y coord on the canvas of this object.
    var _y = parseFloat(y);

    //the radius of this object
    var _radius = parseFloat(radius)

    //the fill boolean indicating whether the circle is outlined or filled
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
    * Will be called by the sketchpad this circle item belongs to. 
    * It draws a circle with a radius that is dependent on the experiment width.
    */
    this.draw = function () {
        if(eval(_condition())) {
            if(_fill == 0){
                var circle = new fabric.Circle({
                    radius: _radius/2, 
                    stroke: _color,
                    strokeWidth: _penwidth,
                });
                circle.set({
                    left: _x + CANVAS.getWidth() / 2 - circle.getWidth() / 2, 
                    top: _y + CANVAS.getHeight() / 2 - circle.getHeight() / 2,
                });
                CANVAS.add(circle);
            } else {
                var circle = new fabric.Circle({
                    radius: _radius/2, 
                    fill: _color, 
                });
                circle.set({
                    left: _x + CANVAS.getWidth() / 2 - circle.getWidth() / 2, 
                    top: _y + CANVAS.getHeight() / 2 - circle.getHeight() / 2,
                });
                CANVAS.add(circle);
            }
        }
    }
}