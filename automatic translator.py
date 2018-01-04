from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import librosa as lib
import librosa.display
import pyaudio
import wave
import math
import scipy.io.wavfile
import datetime
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
        fs, detectvoice = wavfile.read(file_path)
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
        fs, detectvoice = wavfile.read(file_path)
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
def FindLanguage(Record_File_Path, Language_code):
    Response_File_Path = './response voice data/'
    if(Language_code==0):
        playsound(Response_File_Path+'language_response_ch.wav')
    elif(Language_code==1):
        playsound(Response_File_Path+'language_response_en.wav')
    else:
        playsound(Response_File_Path+'language_response_jp.wav')
    e = 1
    Record_File_Path = './record voice/recordvoice_num.wav'
    DetectSound(Record_File_Path)
    
def FindTime(Language_code):  
    Response_File_Path = './response voice data/'
    today = datetime.datetime.now()
    hour = today.hour
    minute = today.minute
    second = today.second
    print(hour,minute,second)
    if(Language_code==0):
        playsound(Response_File_Path+'Now_ch.wav')   
        if(hour>19):
            playsound(Response_File_Path+'2_response_ch.wav') 
        if(hour>9):
            playsound(Response_File_Path+'10_response_ch.wav')
        if(hour%10!=0):
            playsound(Response_File_Path+str(hour%10)+'_response_ch.wav')
        if(hour==0):
            playsound(Response_File_Path+'0_response_ch.wav') 
        playsound(Response_File_Path+'hour_ch.wav')
        
        if(minute>19):
            playsound(Response_File_Path+str(int(minute/10))+'_response_ch.wav') 
        if(minute>9):
            playsound(Response_File_Path+'10_response_ch.wav')
        if(minute%10!=0):
            playsound(Response_File_Path+str(minute%10)+'_response_ch.wav')
        if(minute==0):
            playsound(Response_File_Path+'0_response_ch.wav') 
        playsound(Response_File_Path+'minute_ch.wav')
        
        if(second>19):
            playsound(Response_File_Path+str(int(minute/10))+'_response_ch.wav') 
        if(second>9):
            playsound(Response_File_Path+'10_response_ch.wav')
        if(second%10!=0):
            playsound(Response_File_Path+str(second%10)+'_response_ch.wav') 
        if(second==0):
            playsound(Response_File_Path+'0_response_ch.wav') 
        playsound(Response_File_Path+'second_ch.wav')
        
    elif(Language_code==1):
        playsound(Response_File_Path+'Now_en.wav')
        
        if(hour>19):
            playsound(Response_File_Path+'20_response_en.wav')
            if(hour%10!=0):
                playsound(Response_File_Path+str(hour%10)+'_response_en.wav') 
        else:
            playsound(Response_File_Path+str(hour)+'_response_en.wav') 
        
        if(minute>19):
            if(minute>49):
                playsound(Response_File_Path+'50_response_en.wav') 
            elif(minute>39):
                playsound(Response_File_Path+'40_response_en.wav') 
            elif(minute>29):
                playsound(Response_File_Path+'30_response_en.wav') 
            elif(minute>19):
                playsound(Response_File_Path+'20_response_en.wav') 
            if(minute%10!=0):
                    playsound(Response_File_Path+str(minute%10)+'_response_en.wav') 
        else:        
            playsound(Response_File_Path+str(hour)+'_response_en.wav') 
    else:
        playsound(Response_File_Path+'Now_jp.wav')
        if(hour>19):
            playsound(Response_File_Path+'2_response_jp.wav') 
        if(hour>9):
            playsound(Response_File_Path+'10_response_jp.wav')
        if(hour%10!=0):
            playsound(Response_File_Path+str(hour%10)+'_response_jp.wav')
        if(hour==0):
            playsound(Response_File_Path+'0_response_jp.wav') 
        playsound(Response_File_Path+'hour_jp.wav')
        
        if(minute>19):
            playsound(Response_File_Path+str(int(minute/10))+'_response_jp.wav') 
        if(minute>9):
            playsound(Response_File_Path+'10_response_jp.wav')
        if(minute%10!=0):
            playsound(Response_File_Path+str(minute%10)+'_response_jp.wav') 
        playsound(Response_File_Path+'minute_jp.wav')
        
        if(second>20):
            playsound(Response_File_Path+str(int(second/10))+'_response_jp.wav') 
        if(second>9):
            playsound(Response_File_Path+'10_response_jp.wav')
        if(second%10!=0):
            playsound(Response_File_Path+str(second%10)+'_response_jp.wav') 
        playsound(Response_File_Path+'second_jp.wav')
    
def FindTask(Record_File_Path):
    Compare_File_Path = './comparing voice data/'
    Language_test, fs0 = lib.load(Record_File_Path)
    Language_ch, fs1 = lib.load(Compare_File_Path + 'translate_ch.wav')
    Language_en, fs2 = lib.load(Compare_File_Path + 'translate_en.wav')
    Language_jp, fs3 = lib.load(Compare_File_Path + 'translate_jp.wav')
    Time_ch, fs4 = lib.load(Compare_File_Path + 'time_ch.wav')
    Time_en, fs5 = lib.load(Compare_File_Path + 'time_en.wav')
    Time_jp, fs6 = lib.load(Compare_File_Path + 'time_jp.wav')
    
    MFCC_test = lib.feature.mfcc(y=pre_emphasis(signal = Language_test), sr=fs0, n_mfcc=20)
    MFCC_lang_ch = lib.feature.mfcc(y=Language_ch, sr=fs1, n_mfcc=20)
    MFCC_lang_en = lib.feature.mfcc(y=Language_en, sr=fs2, n_mfcc=20)
    MFCC_lang_jp = lib.feature.mfcc(y=Language_jp, sr=fs3, n_mfcc=20)
    MFCC_time_ch = lib.feature.mfcc(y=Time_ch, sr=fs4, n_mfcc=20)
    MFCC_time_en = lib.feature.mfcc(y=Time_en, sr=fs5, n_mfcc=20)
    MFCC_time_jp = lib.feature.mfcc(y=Time_jp, sr=fs6, n_mfcc=20)
    D_lang_ch, wp_ch = lib.dtw(MFCC_test, MFCC_lang_ch)
    D_lang_en, wp_en = lib.dtw(MFCC_test, MFCC_lang_en)
    D_lang_jp, wp_jp = lib.dtw(MFCC_test, MFCC_lang_jp)
    D_time_ch, wp_ch = lib.dtw(MFCC_test, MFCC_time_ch)
    D_time_en, wp_en = lib.dtw(MFCC_test, MFCC_time_en)
    D_time_jp, wp_jp = lib.dtw(MFCC_test, MFCC_time_jp)
    
    g = D_lang_ch[-1,-1]
    gg = D_lang_en[-1,-1]
    ggg = D_lang_jp[-1,-1]
    Shortest_D = min(D_lang_ch[-1,-1], D_lang_en[-1,-1], D_lang_jp[-1,-1], D_time_ch[-1,-1], D_time_en[-1,-1], D_time_jp[-1,-1])
    if(Shortest_D==D_lang_ch[-1,-1]):
        FindLanguage(Record_File_Path, 0)
    elif(Shortest_D==D_lang_en[-1,-1]):
        FindLanguage(Record_File_Path, 1)
    elif(Shortest_D==D_lang_jp[-1,-1]):
        FindLanguage(Record_File_Path, 2)
    elif(Shortest_D==D_time_ch[-1,-1]):
        FindTime(0)
    elif(Shortest_D==D_time_en[-1,-1]):
        FindTime(1)
    else:
        FindTime(2)
    
def main():
    #Record_File_Path = './record voice/recordvoice.wav'
    #DetectSound(Record_File_Path)
    #FindTask(Record_File_Path)
    
    #FindLanguage(Record_File_Path)

    #Response_File_Path = './response voice data/'
    #playsound(Response_File_Path+'hour_ch.wav')
    e = 1
    FindTime(2)
            
if __name__ == '__main__':
	main()
    