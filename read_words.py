#!/usr/bin/env python3
from tempfile import NamedTemporaryFile

from ukrainian_tts.tts import TTS, Voices, Stress
from pydub import AudioSegment

import os
import sys
import json

START = int(sys.argv[1])
END = int(sys.argv[2])

words = sorted(os.listdir("words"))[START:END]
tts = TTS(device="cpu")


def get_sentences(word: dict):
    title = word['title']
    stresses = word['stresses']
    sentences = [stressed_title(title, stresses)]
    sentences.extend(
        stressed_sentence(sentence, title, stresses[0])
        for sentence in word['html_description'].split("</p><p>")
    )
    return sentences


def stressed_title(title, stresses):
    if len(stresses) == 1:
        stress = stresses[0] - 1
        return f"{title[:stress]}+{title[stress:]}"

    result = ""
    for stress in stresses:
        result += f"{title[:stress-1]}+{title[stress-1:]}"
        if stresses.index(stress)+1 != len(stresses):
            result += " або "
    return result


def stressed_sentence(sentence, title, stress):
    root = title[:stress-1]
    return sentence.replace(root, f"{root}+")


for word_file in words:
    if not word_file.endswith(".json"):
        continue

    file = open(f"words/{word_file}", "r")
    word = json.load(file)

    out = AudioSegment.empty()
    for sentence in get_sentences(word):
        file = NamedTemporaryFile("wb")
        _, _ = tts.tts(sentence, Voices.Dmytro.value, Stress.Dictionary.value, file)

        out += AudioSegment.from_file(file.name)
        out += AudioSegment.silent()
    out.export(f"audio/{word['id']:05d}.wav")
    print(f"{word['title']}: Done.")
