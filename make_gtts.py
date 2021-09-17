import sys
from datetime import datetime, timedelta
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

help = """
ENTER:
'subtitle.srt' 'lang' 'output_file.wav'
"""

if len(sys.argv) < 4 or sys.argv[1] == "-h":
    print(help)
    exit()

subtitle_file = sys.argv[1]
lang = sys.argv[2]
output_file = sys.argv[3]

def load_srt_to_list(file_srt):
    with open(file_srt) as file:
         content = file.read()

    array = []
    groups = content.split('\n\n')
    for idx, item in enumerate(groups):
        item_clean = item.split("\n")
        # Get only non-empty items 
        if len(item_clean) > 2:
            # Split time on start/stop
            time = item_clean[1].split(" --> ")
            start = time[0]
            stop = time[1]
            # 00:00:00,000000 to milliseconds
            start = (datetime.strptime(start, '%H:%M:%S,%f') - datetime.strptime('00', '%H')).total_seconds()*1000
            stop = (datetime.strptime(stop, '%H:%M:%S,%f') - datetime.strptime('00', '%H')).total_seconds()*1000
            # Add item (id, start, stop, text)
            array.append([item_clean[0], start, stop, item_clean[2]])
    return array

srt = load_srt_to_list(subtitle_file)

print("TIME TO FIRST VOICE", srt[0][1])
# Make silent segment before voice
song_all = AudioSegment.silent(duration=srt[0][1])

for idx, item in enumerate(srt):
    print(item)

    # get audio from server
    tts = gTTS(text=item[3], lang=lang, slow=True)

    # convert to file-like object
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp, format="mp3")
    song_duration = int(song.duration_seconds * 1000)

    # Calculating the length of a segment 
    if idx < len(srt) - 1:
        segment_lenght = srt[idx + 1][1] - srt[idx][1]
    else:
        segment_lenght = srt[idx][2] - srt[idx][1]
    silence_duration = segment_lenght - song_duration
    print("*** SEGMENT LENGHT", segment_lenght)
    print("*** SONG DURATION", song_duration)
    print("*** SILENCE DURATION", silence_duration)

    # Make silent part
    silenced_segment = AudioSegment.silent(duration=silence_duration)

    song_new = song + silenced_segment
    if 'song_all' in vars():
        song_all += song_new
    else:
        song_all = song_new

# Save final audio
song_all.export(output_file + ".wav", format="wav")
