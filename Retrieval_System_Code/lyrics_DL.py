import csv

w=open("data/processsedLyrics_DlenUpdated.csv","w")
writer=csv.writer(w)
totalDL=0
with open("data/processedLyrics.csv","r") as f:
    reader=csv.reader(f)
    header=next(reader)
    writer.writerow(header+["DocLength"])
    for row in reader:
        totalDL+=len(row[1].split())
        writer.writerow(row+[len(row[1].split())])
    writer.writerow(["Total DocLength:",totalDL])
    f.close()
w.close()