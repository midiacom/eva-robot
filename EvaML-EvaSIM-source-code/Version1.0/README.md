# EvaML and EvaSIM
We are developing the EvaML, a XML based language for Eva Robot and also, we are creating the EvaSIM (Eva Robot Simulator) in order to test the scripts written in EvaML.
EvaSIM had two source codes, one for Linux and one for Windows. From now on, the EvaSIM code is only one and automatically identifies the type of the operating system being used. In possession of this information, EvaSIM selects the definitions file of its graphical user interface, defines the format (extension) of the audio files and selects the libraries for the function that plays audio files. After identifying the OS being used, the module (plau_audio) provides the "playsound" function suitable for the user's host system.

