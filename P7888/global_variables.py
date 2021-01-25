diagnostics(){
	//read elapsed time in past experiments.
		//define dummy_device that keeps of track of experiment runtime
	//have compilelogic that changes hardware wait times depending on runtimes.

	//calculate Twait segment

	totalruntime = runtime1 + runtime2
	Twait = desiredruntime - totalruntime

	//read analog inputs
	//write analog inputs

	start()
	stop(Twait)
}

switch(sequence_select){
	case 1:
		diagnostics()
	case 2:
		sequence_rabi()

}