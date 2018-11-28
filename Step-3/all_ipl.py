import csv
import glob

resource = glob.glob('/home/sharath_n/Desktop/BigData/Project/ipl_csv/*.csv')

with open('ball-by-ball.csv', 'w', newline='') as myFile:
	myFile.close()

for rFile in resource:
	# reading csv file
	with open(rFile, 'r') as csvfile:
		csvreader = csv.reader(csvfile) # creating a csv reader object
		with open('ball-by-ball.csv', 'a', newline='') as myFile:
			writer = csv.writer(myFile)
			
			# extracting each data row one by one
			for row in csvreader:
				if(len(row) >= 8):
					'''#for r in row:
					row.pop(0)
					row.pop(3)
					if(len(row) == 11):
						row.pop(10)
						row.pop(9)'''
					if(row[8]=='1'):
						row[7] = '7'
					#print([row[1], row[2], row[4], row[6], row[7]])#, r[2], r[4], r[5], r[6], r[7], r[8])
					writer.writerow([row[4], row[6], row[2], row[1], int(row[7])])
				#print(len(row))
			
			#print("Total no. of rows: %d"%(csvreader.line_num)) # get total number of rows
		#print('{0:12s} {1:15s} {2:15s} {3:10s} {4:1s}'.format("Player_Out", "Kind-of-Wicket", "Bowler", "Batsmen", "Extras"))
	csvfile.close()

myFile.close()
