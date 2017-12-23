from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import librosa as lib
import librosa.display
import pyaudio
import wave
import math
import scipy.io.wavfile
# =============================================================================
# Record function
# =============================================================================
def RecordAudio(Audio_output_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 1
    Audio_output_path = Audio_output_path
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE,
                    input = True, frames_per_buffer = CHUNK)
    
    #print("* recording")
    frames = []
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    #print("* done recoding")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(Audio_output_path,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    

def main():
    file_path = './record voice/detectvoice.wav'     
    fs = 16000
    detect = 0
    threshold = 1
    while(detect!=1):
        RecordAudio(file_path)
        fs, detectvoice = wavfile.read('./record voice/detectvoice.wav')
        detectvoice = detectvoice / (2.**15)
        Energy_sum = sum(detectvoice**2)
        print(Energy_sum)
        if(Energy_sum > threshold):
            detect = 1
        else:
            detect = 0
    print("* start recoding")    
    
    stop = 0
    recordvoice = detectvoice
    while(stop!=1):
        RecordAudio(file_path)
        fs, detectvoice = wavfile.read('./record voice/detectvoice.wav')
        detectvoice = detectvoice / (2.**15)
        Energy_sum = sum(detectvoice**2)
        #print(Energy_sum)
        recordvoice = np.hstack((recordvoice,detectvoice))
        if(Energy_sum < threshold):
            stop = 1
        else:
            stop = 0
    e = 1
            
    file_path = './record voice/recordvoice.wav' 
    wave_data = np.int16(recordvoice* (2.**15))
    f = wave.open(file_path, "wb")
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(fs)
    f.writeframes(wave_data.tostring())
    f.close()
            
if __name__ == '__main__':
	main()
    