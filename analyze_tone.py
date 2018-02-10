from __future__ import print_function
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze(summary):
    sid = SentimentIntensityAnalyzer()

    score = 0 
    for s in summary:
        js = sid.polarity_scores(s)
        score += js['pos']
        score -= js['neg']
    if score < 0:
        return " Not Satisfied "
    elif score > 0 :
        return "Satisfied"
    else:
        return "Neutral"
