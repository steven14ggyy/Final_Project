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
# Additional Package
# =============================================================================
from playsound import playsound
# =============================================================================
# Pre-emphasis
# =============================================================================
def pre_emphasis(signal,coefficient=0.97):
    return np.append(signal[0],signal[1:]-coefficient*signal[:-1])
# =============================================================================
# Record function
# =============================================================================
def RecordAudio(Audio_output_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 0.5
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
    
def DetectSound(Record_File_Path):
    file_path = './record voice/detectvoice.wav'     
    fs = 16000
    detect = 0
    threshold = 0.5
    
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
    #print("* start recoding")    
    
    stop = 0
    recordvoice = detectvoice
    while(stop!=1):
        RecordAudio(file_path)
        fs, detectvoice = wavfile.read('./record voice/detectvoice.wav')
        detectvoice = detectvoice / (2.**15)
        Energy_sum = sum(detectvoice**2)
        print(Energy_sum)
        recordvoice = np.hstack((recordvoice,detectvoice))
        if(Energy_sum < threshold):
            stop = 1
        else:
            stop = 0    
    file_path = Record_File_Path 
    wave_data = np.int16(recordvoice* (2.**15))
    f = wave.open(file_path, "wb")
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(fs)
    f.writeframes(wave_data.tostring())
    f.close()
def FindLanguage(Record_File_Path):
    Compare_File_Path = './comparing voice data/'
    Response_File_Path = './response voice data/'
    Language_test, fs0 = lib.load(Record_File_Path)
    Language_ch, fs1 = lib.load(Compare_File_Path + 'translate_ch.wav')
    Language_en, fs2 = lib.load(Compare_File_Path + 'translate_en.wav')
    Language_jp, fs3 = lib.load(Compare_File_Path + 'translate_jp.wav')
    MFCC_test = lib.feature.mfcc(y=pre_emphasis(signal = Language_test), sr=fs0, n_mfcc=20)
    MFCC_ch = lib.feature.mfcc(y=Language_ch, sr=fs1, n_mfcc=20)
    MFCC_en = lib.feature.mfcc(y=Language_en, sr=fs2, n_mfcc=20)
    MFCC_jp = lib.feature.mfcc(y=Language_jp, sr=fs3, n_mfcc=20)
    D_ch, wp_ch = lib.dtw(MFCC_test, MFCC_ch)
    D_en, wp_en = lib.dtw(MFCC_test, MFCC_en)
    D_jp, wp_jp = lib.dtw(MFCC_test, MFCC_jp)
    g = D_ch[-1,-1]
    gg = D_en[-1,-1]
    ggg = D_jp[-1,-1]
    Shortest_D = min(D_ch[-1,-1], D_en[-1,-1], D_jp[-1,-1])
    playsound(Record_File_Path)
    if(Shortest_D==D_ch[-1,-1]):
        playsound(Response_File_Path+'language_response_ch.wav')
    elif(Shortest_D==D_en[-1,-1]):
        playsound(Response_File_Path+'language_response_en.wav')
    else:
        playsound(Response_File_Path+'language_response_jp.wav')
    e = 1
def main():
    Record_File_Path = './record voice/recordvoice.wav'
    DetectSound(Record_File_Path)
    FindLanguage(Record_File_Path)
    
    
            
if __name__ == '__main__':
	main()
    