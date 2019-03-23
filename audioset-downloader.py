import pafy, os, time, ffmpy
import pandas as pd
import soundfile as sf 

dir = os.getcwd()
os.chdir(dir)
#os.chdir("D:\downloader\download_audioset")


file = pd.read_excel('balanced_train_segments.xlsx')

audio_id    = file.iloc[:,0].tolist()[2:]
audio_start = file.iloc[:,1].tolist()[2:]
audio_end   = file.iloc[:,2].tolist()[2:]
#audio_labels = file.iloc[:,3].tolist()[2:]

try:
    data_dir = os.getcwd() + '/audioset/'
    os.chdir(os.getcwd() + '/audioset')
except:
    data_dir = os.getcwd() + '/audioset/'
    os.mkdir(os.getcwd() + '/audioset')
    os.chdir(os.getcwd() + '/audioset')
    
com_link = 'https://www.youtube.com/watch?v='

for i in range(len(audio_id)):
    dl_link    = com_link + audio_id[i]
    start_time = audio_start[i]
    end_time   = audio_end[i]
    
    try:
        video     = pafy.new(dl_link)
        bestaudio = video.getbestaudio()
        audioname = bestaudio.download()
        extension = bestaudio.extension
        #get file extension and convert to .wav for processing later 
        os.rename(audioname, '%s_start_%s_end_%s%s'%(str(i), start_time, end_time, extension))
        audioname  = '%s_start_%s_end_%s%s'%(str(i), start_time, end_time, extension)

        if extension not in ['wav']:
            xindex    = audioname.find(extension)
            audioname = audioname[0:xindex]
            conv2wav  = ffmpy.FFmpeg(
                inputs  = {audioname + extension:None},
                outputs = {audioname + '.wav':None}
                )
            conv2wav.run()
            os.remove(audioname + extension)
        
        file = audioname + '.wav'
        data, sample_rate = sf.read(file)

        total_time  = len(data)/sample_rate
        start_point = sample_rate * start_time
        end_point   = sample_rate * end_time

        sf.write(audio_id[i] + '.wav', data[start_point:end_point], sample_rate)
        #sf.write(file, data[start_point:end_point], sample_rate)
        os.remove(file)

    except:
        print('no urls')
    
time.sleep(5) 
    
