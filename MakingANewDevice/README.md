# Making a New Device

Eventually any labscript experimentalist is going to need to implement a new device. To do this we need to realize that we need to write drivers. Essentially, scripts that allow Labscript to talk to the Device, either through DLLs or Serial Ports or someother mechanism enabled by a python library.

Secondly, we need to understand that once you write this code Labscript needs to know where you wrote your code, and it needs to know what each function is supposed to do. That is, if its mixing up a program for writing to the device vs. taking data we're going to have problems.

So we need to understand what code structure labscript assumes in device communication and two what file structure (and code structure) assumes in your scripts.

##Script Structure

n

##Device Communication Code Structure

