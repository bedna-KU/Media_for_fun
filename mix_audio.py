# -*- coding: utf-8 -*-
from pydub import AudioSegment
import sys

if len(sys.argv) == 4:
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	output = sys.argv[3]
else:
	help = '''
	ENTER:
	"first.wav" "second.wav" "output.wav"
	'''
	print(help)
	exit()

sound1 = AudioSegment.from_file(file1)
sound2 = AudioSegment.from_file(file2)

combined = sound1.overlay(sound2)

combined.export(output, format='wav')
