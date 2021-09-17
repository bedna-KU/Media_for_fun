import datetime
import os 
import sys
from pydub import AudioSegment, effects
from pydub.silence import detect_nonsilent

help = """
ENTER:
'media_file' 'text_file'
"""

# Checking the number of input parameters 
if len(sys.argv) < 3 or sys.argv[1] == "-h":
    print(help)
    exit()

media_file_name = sys.argv[1]
text_file_name = sys.argv[2]

def load_text(text_file_name):
    with open(text_file_name) as file:
        text = file.read()
        text_lines = text.splitlines()
        # Remove empty lines
        text_lines = list(filter(None, text_lines))
    return text_lines

def compute_similarity_text(text, count):
    len_text = len(text)
    max_diff = count
    if (len_text < count + max_diff) and (len_text > count - max_diff):
        return True
    else:
        return False
    
def get_sentences_from_audio(path, text_file_name, offset=300):

    text_lines = load_text(text_file_name)

    # open the audio file using pydub
    audio = AudioSegment.from_wav(path)

    # Normalize audio
    normalizedsound = effects.normalize(audio)  
    audio = normalizedsound
    
    # Detection of loud sections 
    loud = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-30, seek_step=100)
    max_index = len(loud) -1

    print(">>> max_index", max_index)

    # Calculate all lengths of loud sections 
    vocal_len = 0
    for idx, item in enumerate(loud):
        item_time = (item[1] - item[0])
        vocal_len += item_time

    # Calculate all line lengths 
    text_len = 0
    for text_item in text_lines:
        # text_item = text_item.replace(" ", "")
        # text_item = text_item.replace(".", "")
        text_len += len(text_item)

    print(">>> vocal_len", vocal_len, "ms")
    print(">>> text_len", text_len, "chars")
    chars_per_ms = text_len / vocal_len
    print(">>> text_len / vocal_len", chars_per_ms, "chars")

    # Make subtitles
    with open('subtitle.srt', 'w') as srtfile:
        for idx, item in enumerate(loud):
            if len(text_lines[idx]) == 0:
                exit("ERROR: empty string")
            print(">>> IDX", idx)
            start = item[0] - offset
            if start < 0:
                start = 0
            end = item[1] + offset
            if end > max_index:
                end = max_index
            start = item[0]
            end = item[1]
            item_audio = audio[start : end]
            print("VOICE LEN", item[1] - item[0])
            print("LINE LEN", len(text_lines[idx]))
            print("LINE COMP LEN", (item[1] - item[0]) * chars_per_ms)
            print("SIM:", compute_similarity_text(text_lines[idx], (item[1] - item[0]) * chars_per_ms))
            start_time = str(datetime.timedelta(milliseconds=item[0])).replace(".", ",")
            if "," not in start_time:
                start_time = start_time + ",000000"
            stop_time = str(datetime.timedelta(milliseconds=item[1])).replace(".", ",")
            if "," not in stop_time:
                stop_time = stop_time + ",000000"
            out = str(idx + 1) + "\n" + start_time + " --> " + stop_time + "\n" + text_lines[idx] + "\n" + "\n"
            print(out)
            srtfile.write(out)
    return True

status = get_sentences_from_audio(media_file_name, text_file_name)
