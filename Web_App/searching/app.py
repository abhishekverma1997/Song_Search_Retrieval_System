# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 16:32:44 2021

@author: Abhishek
"""

from flask import Flask, render_template, request
from flask import render_template_string
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import math
import copy
import json
import webbrowser
import numpy as np
from datetime import datetime
from ast import literal_eval
from itertools import combinations


app = Flask(__name__)

processedLyrics = pd.read_csv('data/processsedLyrics_DlenUpdated.csv', header=0, names=['ID', 'LYRICS', 'DL'])
mu=2000
dataset = pd.read_csv('data/songDict.csv', error_bad_lines=False, encoding="utf-8")#, names=['ID', 'ARTIST','ARTIST_URL','SONG_NAME','SONG_URL','LYRICS'])
       
def preProcess(query):
    processedQue = query
    stopWordSet = set(stopwords.words('english'))
    # datasets = pd.read_csv("data/songDict.csv")
    # collection = datasets.values.tolist()
    invertedIndex = pd.read_csv("data/invertedIndex.csv")
    invertedIndex = invertedIndex.values.tolist()

    stemmer = PorterStemmer()
    # result = [[] for i in range(len(collection))]
    # print(processedQue)
    processedQue = stemmer.stem(processedQue)
    processedQue = processedQue.split()
    processedQue = [x for x in processedQue if x not in stopWordSet]
    
    # print(processedQue)
    retrievedIndex = [x for x in invertedIndex if x[0] in processedQue]
    # print(retrievedIndex)
    
    return retrievedIndex

def TokenFreq(docid, dictionary):
#     new=literal_eval(retrievedIndex[0][1])
    TF=dictionary[str(docid)] # term frequency of id:133689
#     print(TF)
    return TF

def DirichletSmoothing(token, docid, collectionFreq, dictionary):    
    TF = TokenFreq(docid, dictionary) #// token frequency
    # print(TF)
    # print(docid)
#     print(processedLyrics.loc[docid])
    docLength = processedLyrics.loc[int(docid)]['DL'] #// document length
#     print(DL)
    collectionLength = 18829138
    if (collectionFreq == 0): #// if collection frequency is 0, return 1
        return 1
    else:
        score = (TF + mu * collectionFreq / collectionLength) / (docLength + mu) #// calculate Smoothing
        return score

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/predict')
def predic():
    return render_template('lyr_result.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
   
    if request.method =='POST':
        query = request.form['keyword']
        retrievedIndex = preProcess(query)
        mood = request.form['Mood']
        cnt=[i for i in range(1,30)]
        inx = iter(cnt)
        results = pd.DataFrame(columns=["ID", "Score"])

        for i in range(len(retrievedIndex)):
            dictionary = literal_eval(retrievedIndex[i][1])
            collectionFreq=retrievedIndex[i][2]
            for i in dictionary.keys():
                doc_score = DirichletSmoothing(retrievedIndex[0][0], i, collectionFreq, dictionary)
                # print(doc_score)
                data={"ID":int(i), "Score":doc_score}
                results=results.append(data, ignore_index=True)
                
        final = results.groupby(by=['ID'], as_index=False).sum()           
        # res = {}
        # for doc in range (len(stemmedDoc)):
        #     sums = 0
        #     for qu in range (len(tf)):
        #         if(tf[qu][0] in stemmedDoc[doc]):
        #             ix = indx.index(tf[qu][0])
        #             val = WTD[ix][doc][doc+1]
        #             sums = sums + val
        #     res[doc]=sums
        # result = sorted(res.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        # #result
        # data = []
        # for i in range (len(result)):
        #     if(result[i][1]):
        #         x = result[i][0]
        #         test = (dokumen[x],result[i][1])
        #         data.append(test)

        # print(que)


        # moodtag = pd.read_csv('C:/Users/morni/OneDrive - University of Pittsburgh/Desktop/app/Searching/data/moodTaged.csv', error_bad_lines=False, encoding="utf-8", header=0, names=['ID', 'Main_Mood', 'happy', 'sad', 'romantic', 'calm'])
        # merged_result = pd.merge(final, moodtag, on="ID", how="left")
        # mood_result = merged_result[merged_result['Main_Mood'].isin([mood])]
        
                
        # IdList=[]
        # IdList=mood_result['ID'][0:19]
                
        IdList=[]
        IdList=final['ID'][0:20]

            
        searchedsong = []
        # dataset.loc[33]
        for id in IdList.values:
            searchedsong.append(dataset.loc[id])
            print(searchedsong)
        return render_template('searchResult.html', keyword="".join(query), data = searchedsong, inx=inx, mood=mood)





if __name__ == '__main__':
	app.run(debug=True,use_reloader=False, host='127.0.0.1', port=5000)


