from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
import pickle

def diagraph(path):
    speech_to_text = SpeechToTextV1(
        username='2d655970-82aa-4d54-b6a5-8ea07764fb19',
        password='YCn5FfWboEzt',
        x_watson_learning_opt_out=False)

    with open(join(dirname(__file__), path),'rb') as audio_file:
        x = speech_to_text.recognize(
        audio_file, content_type='audio/wav', timestamps=True,speaker_labels=True,
        word_confidence=True)

    speakers_stamp = x['speaker_labels']
    checks = x['results']

    speakers = {0:[],
            1:[]}

    c = 0 
    for r in range(len(checks)):
        each_check = checks[r]["alternatives"]
        for i in range(len(each_check)):
            ex1 = checks[r]["alternatives"][i]["timestamps"]
            for w in ex1:
                speakers[int(speakers_stamp[c]["speaker"])].append(w[0])
                c+=1
    return speakers
