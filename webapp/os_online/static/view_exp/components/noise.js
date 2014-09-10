/**
* Gabor object class
* This class represents a draw gabot statement that is used in sketchpads to draw a gabor on the screen
*
* @param x - the center X coordinate
* @param y - the center Y coordinate
* @param env - Any of the following: "gaussian", "linear", "circular", "rectangle"
* @param size - size in pixels (default = 96)
* @param stdev - standard deviation in pixels of the gaussian. Only applicable if env = "gaussian"
* @param color1 - human-readable color for the tops
* @param color2 - human-readable color for the throughs
* @param bgmode - specifies whether the background is the average of color1 and color 2 or equal to color2 
* @param condition - draw condition. Item will only be drawn if condition holds
*/
function noise(x, y, env, size, stdev, color1, color2, bgmode, condition) {
    
    var _x = parseFloat(x);

    var _y = parseFloat(y);

    var _env = parseFloat(env);

    var _size = parseFloat(size);

    var _stdev = parseFloat(stdev);

    var _color1 = color1;

    var _color2 = color2;

    //Draw condition. Only if the condition holds, the object will be drawn on screen
    //Has to be parsed first, because this can contain variable names
    var _condition = function () {
        return utils.parseVar(condition);
    }
    
}