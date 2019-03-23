import pafy, time, ffmpy
from pathlib import Path
import pandas as pd
import soundfile as sf 
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

#os.chdir("D:\downloader\download_audioset")

file = pd.read_excel('balanced_train_segments.xlsx')

audio_ids    = file.iloc[:,0].tolist()[2:]
audio_starts = file.iloc[:,1].tolist()[2:]
audio_ends   = file.iloc[:,2].tolist()[2:]
#audio_labels = file.iloc[:,3].tolist()[2:]

data_dir = Path("./audioset").absolute()
data_dir.mkdir(exist_ok=True)
com_link = 'https://www.youtube.com/watch?v='
def map_func(i, audio_id, audio_start, audio_end):
	dl_link = com_link + audio_id
	start_time = audio_start
	end_time = audio_end
	try:
		video = pafy.new(dl_link)
		tile  = video.title
		bestaudio = video.getbestaudio()
		file_path = data_dir / f'{audio_id}_start_{start_time}_end_{end_time}{bestaudio.extension}'
		print(f"start to download {dl_link}")
		audioname = bestaudio.download(filepath=str(file_path))
		print(f"end to download {dl_link}")
		extension = bestaudio.extension

		if extension not in ['wav']:
			xindex    = audioname.find(extension)
			audioname = audioname[0:xindex]
			conv2wav  = ffmpy.FFmpeg(
				inputs  = {audioname + extension:None},
				outputs = {audioname + '.wav':None}
			)
			conv2wav.run()
		#	Path.unlink(audioname + extension)
		
		file = audioname + '.wav'
		#file = audioname		
		data, sample_rate = sf.read(file)

		total_time  = len(data)/sample_rate
		start_point = sample_rate * start_time
		end_point   = sample_rate * end_time

		sf.write(audio_id + '.wav', data[start_point:end_point], sample_rate)
		sf.write(file, data[start_point:end_point], sample_rate)
		#Path.unlink(file)

	except Exception as e:
		print(e)


with ProcessPoolExecutor(8) as executor:
	executor.map(map_func, range(len(audio_ids)), audio_ids, audio_starts, audio_ends, timeout=10)
        
