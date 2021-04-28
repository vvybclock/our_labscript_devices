#HP8648 Driver

This device is a synthesizer that controls bridging frequencies of various devices in our lab.

##Design (Goals) Features 

* To be able to specify the address of the device in the connection table.
* To set the frequency at the BEGINNING of the experiment according to a global variable.
* To set the frequency via GUI in BLACS.

### Setting the Frequency at the Beginning.

This can be accomplished entirely by the `blacs_workers.py`. This can read
data from the HDF shot file and then set the synthesizer frequency
appropriately.