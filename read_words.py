#!/usr/bin/env python3

from ukrainian_tts.tts import TTS, Voices, Stress
from pydub import AudioSegment

import os
import sys
import json

START = int(sys.argv[1])
END = int(sys.argv[2])

words = sorted(os.listdir("words"))[START:END]
tts = TTS(device="cpu")

for word_file in words:
    if not word_file.endswith(".json"):
        continue

    file = open(f"words/{word_file}", "r")
    word = json.load(file)
    text = word['title'] + "\n" + word['description']

    with open(f"audio/{word['id']:05d}.wav", mode="wb") as file:
        _, _ = tts.tts(text, Voices.Dmytro.value, Stress.Dictionary.value, file)
    break
