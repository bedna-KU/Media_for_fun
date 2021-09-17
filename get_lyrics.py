import sys
from azlyrics.azlyrics import lyrics

help = """
ENTER:
'artst' 'song'
"""

# Checking the number of input parameters 
if len(sys.argv) < 3 or sys.argv[1] == "-h":
    exit(help)

# Download lyrics
interpret = sys.argv[1]
song = sys.argv[2]
wd = lyrics(interpret, song)

# Check error
if type(wd) is not dict:
    text_clear = wd[0].strip()
    print(text_clear)
    # Save lyrics
    with open(sys.argv[1].replace(" ", "_") + "-" + sys.argv[2].replace(" ", "_") + ".txt", "w") as text_file:
        text_file.write(text_clear)
else:
    print("ERROR:", wd.get('Error'))

