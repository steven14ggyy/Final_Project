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
import time
from scipy.signal import butter, lfilter, freqz
# =============================================================================
# Additional Package
# =============================================================================
from playsound import playsound

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# =============================================================================
# Pre-emphasis
# =============================================================================
def pre_emphasis(signal,coefficient=0.95):
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
    threshold = 0.6
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

def TranslateNumber(MotherLan, TransLan, Record_File_Path):
    DetectSound(Record_File_Path)
    Response_File_Path = './response voice data/'
    if MotherLan == 0:
        MotherLanAppend = 'ch'
    elif MotherLan == 1:
        MotherLanAppend = 'en'
    elif MotherLan == 2:
        MotherLanAppend = 'jp'
        
    if TransLan == 0:
        TransLanAppend = 'ch'
    elif TransLan == 1:
        TransLanAppend = 'en'
    elif TransLan == 2:
        TransLanAppend = 'jp'
        
    Language_test, fs = lib.load(Record_File_Path)
    compare0, fs0 = lib.load(Response_File_Path + '0_response_' + MotherLanAppend + '.wav')
    compare1, fs1 = lib.load(Response_File_Path + '1_response_' + MotherLanAppend + '.wav')
    compare2, fs2 = lib.load(Response_File_Path + '2_response_' + MotherLanAppend + '.wav')
    compare3, fs3 = lib.load(Response_File_Path + '3_response_' + MotherLanAppend + '.wav')
    compare4, fs4 = lib.load(Response_File_Path + '4_response_' + MotherLanAppend + '.wav')
    compare5, fs5 = lib.load(Response_File_Path + '5_response_' + MotherLanAppend + '.wav')
    compare6, fs6 = lib.load(Response_File_Path + '6_response_' + MotherLanAppend + '.wav')
    compare7, fs7 = lib.load(Response_File_Path + '7_response_' + MotherLanAppend + '.wav')
    compare8, fs8 = lib.load(Response_File_Path + '8_response_' + MotherLanAppend + '.wav')
    compare9, fs9 = lib.load(Response_File_Path + '9_response_' + MotherLanAppend + '.wav')
#    plt.plot(Language_test)
#    plt.show()
    
    Language_test = pre_emphasis(signal = Language_test)
#    plt.plot(Language_test)
#    plt.show()
    
#    Language_test = butter_lowpass_filter(Language_test, 1000, fs, 6)
#    plt.plot(Language_test)
#    plt.show()
    
    test = Language_test
    
#    test = []    
#    for i in range(len(Language_test)-1):
#        if not((Language_test[i] < 0.005 and Language_test[i] > -0.005) and (Language_test[i+1] < 0.005 and Language_test[i+1] > -0.005)):
#            test = np.hstack((test,Language_test[i]))
            
#    plt.plot(test)
#    plt.show()
    
    D_compare0, wp_0 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare0, sr=fs0, n_mfcc=30))
    D_compare1, wp_1 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare1, sr=fs1, n_mfcc=30))
    D_compare2, wp_2 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare2, sr=fs2, n_mfcc=30))
    D_compare3, wp_3 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare3, sr=fs3, n_mfcc=30))
    D_compare4, wp_4 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare4, sr=fs4, n_mfcc=30))
    D_compare5, wp_5 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare5, sr=fs5, n_mfcc=30))
    D_compare6, wp_6 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare6, sr=fs6, n_mfcc=30))
    D_compare7, wp_7 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare7, sr=fs7, n_mfcc=30))
    D_compare8, wp_8 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare8, sr=fs8, n_mfcc=30))
    D_compare9, wp_9 = lib.dtw(lib.feature.mfcc(y=test, sr=fs, n_mfcc=30), lib.feature.mfcc(y=compare9, sr=fs9, n_mfcc=30))
        
    Shortest_D = min(D_compare0[-1,-1], D_compare1[-1,-1],\
                     D_compare2[-1,-1], D_compare3[-1,-1],\
                     D_compare4[-1,-1], D_compare5[-1,-1],\
                     D_compare6[-1,-1], D_compare7[-1,-1],\
                     D_compare8[-1,-1], D_compare9[-1,-1])
        
    if Shortest_D == D_compare0[-1,-1]: 
        playsound(Response_File_Path+'0_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare1[-1,-1]:
        playsound(Response_File_Path+'1_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare2[-1,-1]:
        playsound(Response_File_Path+'2_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare3[-1,-1]:
        playsound(Response_File_Path+'3_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare4[-1,-1]:
        playsound(Response_File_Path+'4_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare5[-1,-1]:
        playsound(Response_File_Path+'5_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare6[-1,-1]:
        playsound(Response_File_Path+'6_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare7[-1,-1]:
        playsound(Response_File_Path+'7_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare8[-1,-1]:
        playsound(Response_File_Path+'8_response_' + TransLanAppend + '.wav')
    elif Shortest_D == D_compare9[-1,-1]:
        playsound(Response_File_Path+'9_response_' + TransLanAppend + '.wav')  
                    
    return D_compare0[-1,-1], D_compare1[-1,-1], D_compare2[-1,-1], D_compare3[-1,-1], D_compare4[-1,-1], D_compare5[-1,-1], D_compare6[-1,-1], D_compare7[-1,-1], D_compare8[-1,-1], D_compare9[-1,-1]

def FindLanguage(Record_File_Path, Language_code):
    Response_File_Path = './response voice data/'
    if(Language_code==0):
        playsound(Response_File_Path+'language_response_ch.wav')
        time.sleep(0.5)
        playsound(Response_File_Path+'language_select_ch.wav')
        char_append = 'ch'
    elif(Language_code==1):
        playsound(Response_File_Path+'language_response_en.wav')
        time.sleep(0.5)
        playsound(Response_File_Path+'language_select_en.wav')
        char_append = 'en'
    else:
        playsound(Response_File_Path+'language_response_jp.wav')
        time.sleep(0.5)
        playsound(Response_File_Path+'language_select_jp.wav')
        char_append = 'jp'
        
    DetectSound(Record_File_Path)
    Compare_File_Path = './comparing voice data/'
    Language_test, fs0 = lib.load(Record_File_Path)
    MFCC_test = lib.feature.mfcc(y=pre_emphasis(signal = Language_test), sr=fs0, n_mfcc=20)
    
    
    if(Language_code==0):
        Language_en_ch, fs1 = lib.load(Compare_File_Path + 'language_en_ch.wav')
        Language_jp_ch, fs2 = lib.load(Compare_File_Path + 'language_jp_ch.wav')
        MFCC_lang_en_ch = lib.feature.mfcc(y=Language_en_ch, sr=fs1, n_mfcc=20)
        MFCC_lang_jp_ch = lib.feature.mfcc(y=Language_jp_ch, sr=fs2, n_mfcc=20)
        D_lang_en_ch, wp_en_ch = lib.dtw(MFCC_test, MFCC_lang_en_ch)
        D_lang_jp_ch, wp_jp_ch = lib.dtw(MFCC_test, MFCC_lang_jp_ch)
        compare1 = D_lang_en_ch[-1, -1]
        compare2 = D_lang_jp_ch[-1, -1]
        if(compare1<compare2):
            translate_lang = 1
        else:
            translate_lang = 2
    elif(Language_code==1):
        Language_ch_en, fs1 = lib.load(Compare_File_Path + 'language_ch_en.wav')
        Language_jp_en, fs2 = lib.load(Compare_File_Path + 'language_jp_en.wav')
        MFCC_lang_ch_en = lib.feature.mfcc(y=Language_ch_en, sr=fs1, n_mfcc=20)
        MFCC_lang_jp_en = lib.feature.mfcc(y=Language_jp_en, sr=fs2, n_mfcc=20)
        D_lang_ch_en, wp_ch_en = lib.dtw(MFCC_test, MFCC_lang_ch_en)
        D_lang_jp_en, wp_jp_en = lib.dtw(MFCC_test, MFCC_lang_jp_en)
        compare1 = D_lang_ch_en[-1, -1]
        compare2 = D_lang_jp_en[-1, -1]
        if(compare1<compare2):
            translate_lang = 0
        else:
            translate_lang = 2
    else:
        Language_ch_jp, fs1 = lib.load(Compare_File_Path + 'language_ch_jp.wav')
        Language_en_jp, fs2 = lib.load(Compare_File_Path + 'language_en_jp.wav')
        MFCC_lang_ch_jp = lib.feature.mfcc(y=Language_ch_jp, sr=fs1, n_mfcc=20)
        MFCC_lang_en_jp = lib.feature.mfcc(y=Language_en_jp, sr=fs2, n_mfcc=20)
        D_lang_ch_jp, wp_ch_jp = lib.dtw(MFCC_test, MFCC_lang_ch_jp)
        D_lang_en_jp, wp_en_jp = lib.dtw(MFCC_test, MFCC_lang_en_jp)
        compare1 = D_lang_ch_jp[-1, -1]
        compare2 = D_lang_en_jp[-1, -1]
        if(compare1<compare2):
            translate_lang = 0
        else:
            translate_lang = 1
        
    playsound(Response_File_Path+'say_number_'+char_append+'.wav')
    TranslateNumber(Language_code, translate_lang, Record_File_Path)
    
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
            playsound(Response_File_Path+str(int(second/10))+'_response_ch.wav') 
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
            playsound(Response_File_Path+str(minute)+'_response_en.wav') 
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
    D_lang_ch, wp_lang_ch = lib.dtw(MFCC_test, MFCC_lang_ch)
    D_lang_en, wp_lang_en = lib.dtw(MFCC_test, MFCC_lang_en)
    D_lang_jp, wp_lang_jp = lib.dtw(MFCC_test, MFCC_lang_jp)
    D_time_ch, wp_time_ch = lib.dtw(MFCC_test, MFCC_time_ch)
    D_time_en, wp_time_en = lib.dtw(MFCC_test, MFCC_time_en)
    D_time_jp, wp_time_jp = lib.dtw(MFCC_test, MFCC_time_jp)
    
#    D1 = D_lang_ch[wp_lang_ch[-1, 0], wp_lang_ch[-1, 1]]
#    D2 = D_lang_en[wp_lang_en[-1, 0], wp_lang_en[-1, 1]]
#    D3 = D_lang_jp[wp_lang_jp[-1, 0], wp_lang_jp[-1, 1]]
#    D4 = D_time_ch[wp_time_ch[-1, 0], wp_time_ch[-1, 1]]
#    D5 = D_time_en[wp_time_en[-1, 0], wp_time_en[-1, 1]]
#    D6 = D_time_jp[wp_time_jp[-1, 0], wp_time_jp[-1, 1]]
#    
#    Shortest_D = min(D1, D2, D3, D4, D5, D6)
#    if(Shortest_D==D1):
#        FindLanguage(Record_File_Path, 0)
#    elif(Shortest_D==D2):
#        FindLanguage(Record_File_Path, 1)
#    elif(Shortest_D==D3):
#        FindLanguage(Record_File_Path, 2)
#    elif(Shortest_D==D4):
#        FindTime(0)
#    elif(Shortest_D==D5):
#        FindTime(1)
#    elif(Shortest_D==D6):
#        FindTime(2)
    
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
    elif(Shortest_D==D_time_jp[-1,-1]):
        FindTime(2)
    
Record_File_Path = './record voice/recordvoice.wav'
while(1):
    DetectSound(Record_File_Path)
    FindTask(Record_File_Path)
#while(1):
    #a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = TranslateNumber(0, 1, Record_File_Path)

    