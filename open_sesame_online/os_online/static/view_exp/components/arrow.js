/**
* Arrow object class
* This class represents a draw arrow statement that is used in sketchpads to draw a arrow on the screen
*
* @param sx - the left coordinate
* @param sy - the top coordinate
* @param ex - the right coordinate
* @param ey - the bottom coordinate
* @param penwidth - line thickness
* @param color - the color of this arrow
* @param size - the length of the arrowhead lines
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function arrow(sx, sy, ex, ey, penwidth, color, size, condition) {
    
    //x coord on the canvas of this object.
    var _sx = parseFloat(sx);

    //y coord on the canvas of this object.
    var _sy = parseFloat(sy);

    //the width of this object
    var _ex = parseFloat(ex)

    //the height of this object
    var _ey = parseFloat(ey)

    //width of line
    var _penwidth = parseFloat(penwidth);

    //The color of this circle
    var _color = color;

    //length of the arrowhead
    var _size = size;

    //Draw condition. Only if the condition holds, the object will be drawn on screen
    //Has to be parsed first, because this can contain variable names
    var _condition = function () {
        return utils.parseVar(condition);
    }

    var _left = _sx + CANVAS.getWidth()/2;

    var _top = _sy + CANVAS.getHeight()/2 ;

    var _right = _ex + CANVAS.getWidth()/2;

    var _bottom = _ey + CANVAS.getHeight()/2;

    /**
    * Draw function.
    * Will be called by the sketchpad this arrow item belongs to. 
    * It draws an arrow.
    */
    this.draw = function () {
        if(eval(_condition())) {
            // var arrow = new fabric.Path('M ' + _left + ' ' + _top + 'L ' + _right + ' ' + _bottom + 'M ' + _right + ' ' + _bottom + 'L 45 52 M' + _right + ' ' + _bottom + 'L 45 -52 z', {
            //     stroke: 'red',
            //     strokeWidth: 1,
            //     fill: false
            // });
             var arrow = new fabric.Path('M ' + _left + ' ' + _top + 'L ' + _right + ' ' + _bottom + 'M ' + _right + ' ' + _bottom + 'L 45 52 M' + _right + ' ' + _bottom + 'L 45 -52 z', {
                stroke: _color,
                strokeWidth: _penwidth,
                fill: false
            });
            CANVAS.add(arrow);            
        }
    }
}