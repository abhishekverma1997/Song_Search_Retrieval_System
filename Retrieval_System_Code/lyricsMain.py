import csv
import lyricsStemming


ly=lyricsStemming.lyricsStemming()
songDict={}
processedLyrics={}
a=0
song_header=[]

fw1=open("data/processedLyrics.csv",'w')
fw2=open("data/songDict.csv",'w')
w1=csv.writer(fw1)
w2=csv.writer(fw2)
w1.writerow(["id","ProcessedLyrics"])

with open("data/combined-csv-files.csv") as f:
    reader=csv.reader(f)
    song_header=next(reader)
    song_header.insert(0,"id")
    w2.writerow(song_header)
    for row in reader:
        r=[]
        if len(row)>5:
            line=""
            for i in range(len(row)):
                if i>=4:
                    line+=row[i]
            r=row[:4]
            r.append(line)
        else:
            r=row
        songDict[a]=r
        w2.writerow([a]+row)
        a+=1


a=0
for i in songDict:
    temp=ly.striplyrics(songDict[i][-1])   #temp is a string
    temp=ly.removeStopwords(temp)          #temp becomes a list
    temp=ly.normalize(temp)
    processedLyrics[i]=temp
    w1.writerow([i,temp])
    a+=1
    if a%10000==0:
        print("finish ",a/10000)

# with open("data/processedLyrics.csv",'w') as fw:
#     fw.write(str(processedLyrics))
#     fw.close()
# with open("data/songDict.csv",'w') as fw:
#     fw.write(str(songDict))
#     fw.close()
# # read dict from txt as:
# # with open("data/processedLyrics.txt",'r') as fr:
#     # dic=eval(fr.read())
#     # fr.close()
fw1.close()
fw2.close()

