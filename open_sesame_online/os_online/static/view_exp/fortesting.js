utils.canvasInit(1024, 768);
var CANVAS = new fabric.StaticCanvas("canvas");

var globalVars = [];
globalVars["background"] = "black";

var cycles = [
	{
		"[var1]": "Pen",
		"[cr]":"65",
	},
	{
		"[var1]": "Work",
		"[cr]":"66",
	},
	{
		"[var1]": "Couch",
		"[cr]":"65",
	},
	{
		"[var1]": "Chair",
		"[cr]":"65",
	},
	{
		"[var1]": "Play",
		"[cr]":"66",
	},
];

var t = new text_display("text", undefined, undefined, undefined, "haha", undefined, undefined, undefined);
var log = new logger("log", undefined);
var seq = new sequence("seq", [t, log], [true, true]);
var lo = new loop ("lo", 1, 0, undefined, seq, "false", [], 1, "sequential", undefined);

var exp= new sequence("exp", [lo], [true]);

var MASTER = new Experiment(exp);
MASTER.run();