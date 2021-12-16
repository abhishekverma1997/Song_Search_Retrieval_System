import csv
import lyricsStemming

moodDict={}
moodDict["happy"]=[]
moodDict["sad"]=[]
moodDict["romantic"]=[]
moodDict["calm"]=[]
mood=lyricsStemming.lyricsStemming()
with open("data/Mood.csv") as f:
    reader=csv.reader(f)
    mood_header=next(reader)
    for row in reader:
        if row[0]!="":
            moodDict["happy"].append(row[0])
        if row[1]!="":
            moodDict["sad"].append(row[1])
        if row[2]!="":
            moodDict["romantic"].append(row[2])
        if row[3]!="":
            moodDict["calm"].append(row[3])
for i in moodDict:
    moodDict[i]=mood.normalize(moodDict[i])
print("finish stem mood words")

lyricsDict={}
songMood={}
fw=open("data/moodTaged.csv","w")
wr=csv.writer(fw)
wr.writerow(["id","Main_mood","happy","sad","romantic","calm"])
with open("data/processedLyrics.csv",'r') as fr:
    reader=csv.reader(fr)
    header=next(reader)
    for row in reader:
        lyricsDict[row[0]]=row[1]
    fr.close()
for i in lyricsDict:    # i is songID
    songMood[i]={}
    if int(i)%10000==0:
        print("finish ", int(i)/10000)
    for j in lyricsDict[i].split():     # j is each word in every song
        for k in moodDict:      #k is happy, sad, romantic, calm
            if k not in songMood[i]:
                songMood[i][k]=0
            if j in moodDict[k]:
                songMood[i][k]+=1
    #print(i," ",songMood[i])
    l=[i]
    if(songMood[i]):
        mainMood=max(songMood[i].values())
        for j in songMood[i]:
            if songMood[i][j]==mainMood:
                l.append(j)
    else:
        l.append("")
    wr.writerow(l+list(songMood[i].values()))