/**
* KeyListener
* KeyListeners run globally throughout the entire document,
* so in order to make the document respond to keypresses only 
* at a certain time, we need to make our way down to the
* currentObject and ask it if the document has to do something with the 
* keypress or just ignore it.
* 
* @param evt - the key event
*/
document.onkeypress = function(evt) {
	
	//The timestamp of when this key is pressed. Is used to compute reaction times
	var time = Date.now();

	//The key event
	evt = evt || window.event;	
	//The object that's currently being played.
	object = MASTER.getCurrentObject();	

	//Checks whether the experiment has ended and if the current object is allowed
	//to respond to keypresses.
	if(MASTER.getExperimentEnded() == 0) {
		if(MASTER.getCurrentObject() instanceof keyboard_response || MASTER.getCurrentObject().getDuration() == "keypress") {
			object.keyDown(String.fromCharCode(evt.which), time);
		} 
	}
}