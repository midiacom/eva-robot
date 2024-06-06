import platform

if platform.system() == "Linux":
    from playsound import playsound as ps
    print("Linux audio library loaded")
    def playsound(audio_file, block = True):
        ps(audio_file, block)

if platform.system() == "Windows":
    print("Windows audio library loaded")
    # playing audio
    import sounddevice as sd
    import soundfile as sf
    # my playsound function
    def playsound(file, block = True):
        # Extract data and sampling rate from file
        data, fs = sf.read(file, dtype='float32')  
        sd.play(data, fs)
        if block == True: status = sd.wait()  # Wait until file is done playing