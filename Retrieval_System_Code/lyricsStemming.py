import csv
import string
from nltk.stem import *
from nltk.stem.porter import *

class lyricsStemming:
    def  __init__(self):
        return

    def removeStopwords(self,lyrics):
        stopword=[]
        with open("data/stopword.txt") as f:
            l=f.readline()
            while l:
                stopword.append(l.strip())
                l=f.readline()
        lyrics_list=lyrics.split()
        lyrics_noStopwords=[]
        for i in lyrics_list:
            if i not in stopword:
                lyrics_noStopwords.append(i)
        return lyrics_noStopwords

    def striplyrics(self,lyrics):
        for i in string.punctuation:
            lyrics=lyrics.replace(i," ")
        return lyrics

    def normalize(self,lyrics):
        stemmer=PorterStemmer()
        nomalizedLyrics=[]
        for i in lyrics:
            a=i.lower()
            a=stemmer.stem(a)
            nomalizedLyrics.append(a)
        return " ".join(nomalizedLyrics)



