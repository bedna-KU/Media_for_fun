#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import sys
import time

__author__ = "Mario Chorvath"
__license__ = "GPL"

"""
Translate text over https://lindat.mff.cuni.cz/services/translation
Czech, English, French, German, Polish, Rusian
"""

if len(sys.argv) == 5:
    input_file = sys.argv[1]
    input_lang = sys.argv[2]
    output_file = sys.argv[3]
    output_lang = sys.argv[4]
else:
    help = """
    ENTER
    input_file input_lang output_file output_lang
    """
    print(help)
    exit()

with open(input_file) as f:
    content = f.readlines()

headers = {
    'accept':'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

print(content)
# exit()

translated_content = []
with open(output_file, 'w') as the_file:
    for line in content:
        # if empty line translated line = empty line
        if line == "\n":
            translated = "\n"
            translated_content.append(translated)
        else:
            line = line.replace("\n", "")
            data = {
                'input_text':line
            }
            output = requests.post('https://lindat.mff.cuni.cz/services/translation/api/v2/languages/?src='
                                    + input_lang + '&tgt=' + output_lang,
                                    headers=headers, data=data)

            translated = output.json()[0]
            translated_content.append(translated)
            if translated[-1] != "\n":
                translated += "\n"
        print(translated)
        the_file.write(translated)
print(translated_content)