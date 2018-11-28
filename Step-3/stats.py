import csv

x = []
with open('player-stat.csv', 'w', newline='') as fp:
	writer = csv.writer(fp)


	with open('ball-by-ball.csv', 'r', newline='') as myFile:
		reader1 = csv.reader(myFile)
		for row in reader1:
			with open('/home/sharath_n/Desktop/BigData/Project/Step-1/batting.csv', 'r', newline='') as csc:
				reader2 = csv.reader(csc)
				#for row in reader1:
				for col in reader2:
					if(col[0]==row[0]):
						row.insert(2, col[7])
						row.insert(3, col[9])
						#print(row)
						#writer.writerow(row)
						break
			
			csc.close()
			with open('/home/sharath_n/Desktop/BigData/Project/Step-1/bowling.csv', 'r', newline='') as cs:
				reader2 = csv.reader(cs)
				#for row in reader1:
				for col in reader2:
					if(col[0]==row[1]):
						row.insert(4, col[9])
						row.insert(5, col[10])
						row.insert(6, col[11])
						#print(row)
						writer.writerow(row)
						break
			
			cs.close()
	
	myFile.close()

fp.close()

