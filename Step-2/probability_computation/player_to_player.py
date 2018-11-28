import sys
import csv
from collections import defaultdict
dic = defaultdict(list)
newdic = dict()
with open('ipl.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
    	b = [row[2],row[3]#value of dict 
    	dic[row[0],row[1]].append(b)#key of dict

csvFile.close()
csvfile = open('player_to_player.csv','w')
fieldnames = ['batsman', 'bowler', '0','1','2','3','4','6','out','batclustno','bowlclustno','balls']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()


for key,values in dic.items():
	#print(key,type(key),key[0],key[1])
	dot = 0
	one = 0
	two = 0
	three = 0
	four = 0
	six = 0
	wick = 0
	balls = 0
	for i in values:
		p = i[0]
		#print(i,type(i),i[0],i[1])
		if p == '0':
			dot = dot+1
		elif p == '1':
			one = one+1
		elif p == '2':
			two = two+1
		elif p == '3':
			three = three+1
		elif p == '4':
			four = four+1
		elif p == '6':
			six = six+1
		if i[1] == '1':
			wick = wick +1
		balls = balls +1
	#print(key,dot,one,two,three,four,six,wick,balls)
	#print(key,wick)
	batclustno = 0
	bowlclusrno = 0
	with open('../cluster_files/bat_clusters.csv') as file1:
		read = csv.reader(file1)
		for row in read:
			if row[0] == key[0]:
				batclustno = row[1]
				break
	with open('../cluster_files/bowl_clusters.csv') as file2:
		read = csv.reader(file2)
		for row in read:
			if row[0] == key[1]:
				bowlclustno = row[1]
				break
	#newdic[key] = [dot/balls,one/balls,two/balls,three/balls,four/balls,six/balls,wick/balls]
	writer.writerow({'batsman':key[0],'bowler':key[1],'0':dot/balls,'1':one/balls,'2':two/balls,'3':three/balls,'4':four/balls,'6':six/balls,'out':wick/balls,'batclustno':batclustno,'bowlclustno':bowlclustno,'balls':balls})
	
	
	
'''for key in sorted(newdic.keys()):
    print ("%s: %s" % (key, newdic[key]))'''
