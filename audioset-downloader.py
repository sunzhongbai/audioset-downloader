import pafy, os, shutil, time, ffmpy
import pandas as pd
import soundfile as sf 

dir = os.getcwd()
os.chdir(dir)
#os.chdir("D:\downloader\download_audioset")


file = pd.read_excel('balanced_train_segments.xlsx')

audio_id = file.iloc[:,0].tolist()[2:]
audio_start = file.iloc[:,1].tolist()[2:]
audio_end = file.iloc[:,2].tolist()[2:]
audio_labels = file.iloc[:,3].tolist()[2:]




try:
    data_dir = os.getcwd() + '/audioset/'
    os.chdir(os.getcwd() + '/audioset')
except:
    data_dir = os.getcwd() + '/audioset/'
    os.mkdir(os.getcwd() + '/audioset')
    os.chdir(os.getcwd() + '/audioset')
    
com_link = 'https://www.youtube.com/watch?v='
for i in range(len(audio_id)):
    dl_link = com_link + audio_id[i]
    start = audio_start[i]
    end = audio_end[i]
    
    try:
        video = pafy.new(dl_link)
        bestaudio = video.getbestaudio()
        filename  = bestaudio.download()
        extension = bestaudio.extension
        
        os.rename(filename,'%s%s'%(str(audio_id[i]),extension))
        filename='%s%s'%(str(audio_id[i]),extension)


        if extension not in ['wav']:
            xindex = filename.find(extension)
            filename = filename[0:xindex]
            ff = ffmpy.FFmpeg(
                inputs = {filename + extension: None},
                outputs = {filename + '.wav': None}
                )
            ff.run()
            os.remove(filename + extension)

        file = filename + '.wav'
        data, samplerate = sf.read(file)
        totalframes = len(data)
        totalseconds = totalframes/samplerate
        startsec = start
        startframe = samplerat * startsec
        endsec = end
        endframe = samplerate * endsec
        sf.write(file, data[startframe:endframe], samplerate)
        os.remove(file)

    except:
        print('no urls')
    
    
