from pydub import AudioSegment
from pydub.playback import play
import os


root_dir = '/media/ljy/304610E34610AB9A/Users/ljy/Music'
# root_dir 中后缀名为 .flac 和 .mp3 的文件
music_files = []
for file in os.listdir(root_dir):
    if file.endswith('.flac') or file.endswith('.mp3'):
        music_files.append(os.path.join(root_dir, file))

i=0
for music_file in music_files:
    if i==0 or i==1:
        i+=1
        continue
    print(f"Playing {music_file}")
    audio = AudioSegment.from_file(music_file)
    # 提高采样率
    audio = audio.set_frame_rate(256000)
    # 使用 24bit 采样
    audio = audio.set_sample_width(3)
    # 提高比特率
    audio = audio.set_channels(2)
    # 降低噪声
    play(audio)

