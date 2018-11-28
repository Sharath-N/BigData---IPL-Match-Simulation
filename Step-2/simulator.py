	import random
import csv
import pandas as pd  

bat_clust = dict()
bowl_clust = dict()
team1 = []
team2 = []
files = pd.read_csv('probability_computation/player_to_player.csv')  #Reading from the probability file 
for i in range(len(files)):
	batname = files.loc[i].batsman.strip()     #Keys of dictionary are batsman name and values are cluster number
	bat_clust[batname] = files.loc[i].batclustno
	bowlname = files.loc[i].bowler.strip()   #Keys of dictionary are bowler name and values are cluster number
	bowl_clust[bowlname] = files.loc[i].bowlclustno

#Input for the match to be simulated
with open('squad1.csv') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
	for row in reader:
		team1.append(row[0])
		team2.append(row[1])
csvFile.close()

clust = pd.read_csv('probability_computation/clust_to_clust.csv')
clust_prob = pd.DataFrame(columns=['batclustno','bowlclustno','0', '1', '2', '3', '4',  '6','notout'])
for i in range(len(clust)):
	clust_prob.at[i] = [None for n in range(9)]
	clust_prob.at[i,'batclustno'] = clust.at[i,'batclustno']	       
	clust_prob.at[i,'bowlclustno'] = clust.at[i,'bowlclustno']
	clust_prob.at[i,'0'] = float(clust.at[i,'0'])                            #Finding cumulative probabilities
	clust_prob.at[i,'1'] = float(clust.at[i,'1']) + float(clust.at[i,'0'])
	clust_prob.at[i,'2'] = float(clust.at[i,'2']) + float(clust_prob.at[i,'1'])
	clust_prob.at[i,'3'] = float(clust.at[i,'3']) + float(clust_prob.at[i,'2'])
	clust_prob.at[i,'4'] = float(clust.at[i,'4']) + float(clust_prob.at[i,'3'])
	clust_prob.at[i,'6'] = float(clust.at[i,'6']) + float(clust_prob.at[i,'4'])
	clust_prob.at[i,'notout'] = 1 - float(clust.at[i,'out'])

player_prob = pd.read_csv('player_cumprob.csv')

def playerprob(batsman,bowler):
	row = player_prob.loc[player_prob['batsman'] == batsman].loc[player_prob['bowler'] == bowler]
	rand = random.random()
	if rand <= float(row['0']):                         
		return 0				    
	elif  rand <= float(row['1']):                     
		return 1
	elif rand <= float(row['2']):
		return 2
	elif rand <= float(row['3']):
		return 3
	elif  rand <= float(row['4']):
		return 4
	elif rand <= float(row['6']):
		return 6

def clusterprob(bat_clust_no,bowl_clust_no):
	row = clust_prob.loc[clust_prob['batclustno'] == bat_clust_no].loc[clust_prob['bowlclustno'] == bowl_clust_no]
	rand = random.random()
	#print(bat_clust_no,bowl_clust_no)
	#print(row)
	#print(float(row['0']))
	if rand <= float(row['0']):                         
		return 0				    
	elif  rand <= float(row['1']):                     
		return 1
	elif rand <= float(row['2']):
		return 2
	elif rand <= float(row['3']):
		return 3
	elif  rand <= float(row['4']):
		return 4
	elif rand <= float(row['6']):
		return 6

	

def innings1(team1, team2):
	striker = team1[0]
	non_striker = team1[1]
	bowler = team2[len(team2)-1]
	nextbatsman = 2
	wick = 0
	runs = 0
	overs = 0
	prob = 0
	count = 2
	nprob = 1
	dic = {}
	dic[striker] = 1
	dic[non_striker]=1
	while(overs<20 and wick < 10):
		balls = 1
		cl = 0
		while(balls<6 and wick <10):
			try:
				row = player_prob.loc[player_prob['batsman'] == striker].loc[player_prob['bowler'] == bowler]
				prob = float(row['notout'])
			except:
				row = clust_prob.loc[clust_prob['batclustno'] == bat_clust[striker]].loc[clust_prob['bowlclustno'] == bowl_clust[bowler]]
				prob = float(row['notout'])
				cl = 1
				
			score = 0
			flag = 0
			nprob = nprob*prob
			dic[striker] = dic[striker]*prob
			if (dic[striker] > 0.5):
				if cl==0:
					if (int(row['balls'])>=15):
						score = playerprob(striker,bowler)
					else:
						score = clusterprob(bat_clust[striker],bowl_clust[bowler])
						
				else:
					#print(striker,bowler)
					score = clusterprob(bat_clust[striker],bowl_clust[bowler])
			elif dic[striker] < 0.5:
				wick = wick+1
				striker = team1[nextbatsman]
				nextbatsman = (nextbatsman+1)%11
				flag = 1
				dic[striker] = 1
			if(flag==0):
				runs = runs+score
				if (score==1 or score == 3):
					striker,non_striker = non_striker,striker
			balls = balls+1
		striker,non_striker = non_striker,striker                 
		bowler = team2[len(team2)-count]                    
		count = (count+1)%5 + 1 
		overs = overs+1
		print("{0:10d} {1:10d}".format(overs, runs))
		#print(overs, runs)
	return runs,wick


def innings2(team1, team2,runs1):
	striker = team1[0]
	non_striker = team1[1]
	bowler = team2[len(team2)-1]
	nextbatsman = 2
	wick = 0
	runs = 0
	overs = 0
	prob = 0
	count = 2
	nprob = 1
	dic = {}
	dic[striker] = 1
	dic[non_striker]=1
	while(overs<20 and wick < 10):
		balls = 1
		cl = 0
		
		while(balls<6 and runs<=runs1 and wick <10):
			try:
				row = player_prob.loc[player_prob['batsman'] == striker].loc[player_prob['bowler'] == bowler]
				prob = float(row['notout'])
			except:
				row = clust_prob.loc[clust_prob['batclustno'] == bat_clust[striker]].loc[clust_prob['bowlclustno'] == bowl_clust[bowler]]
				prob = float(row['notout'])
				cl = 1
				
			score = 0
			flag = 0
			nprob = nprob*prob
			dic[striker] = dic[striker]*prob
			#print(striker,dic[striker])
			if (dic[striker] > 0.5):
				if cl==0:
					if (int(row['balls'])>=15):
						score = playerprob(striker,bowler)
					else:
						score = clusterprob(bat_clust[striker],bowl_clust[bowler])
						
				else:
					#print(striker,bowler)
					score = clusterprob(bat_clust[striker],bowl_clust[bowler])
			elif dic[striker] < 0.5:
				wick = wick+1
				striker = team1[nextbatsman]
				nextbatsman = (nextbatsman+1)%11
				flag = 1
				dic[striker] = 1
			if(flag==0):
				runs = runs+score
				if (score==1 or score == 3):
					striker,non_striker = non_striker,striker
			balls = balls+1
		striker,non_striker = non_striker,striker                 
		bowler = team2[len(team2)-count]                    
		count = (count+1)%5 + 1 
		overs = overs+1
		print("{0:10d}|{1:10d}".format(overs, runs))
		#print(overs, runs)
		if (runs>runs1):
			break
	return runs,wick

print("First Innings")
print("Overs{:10d}|{:10d}Runs")
runs1 ,wicks1 = innings1(team1,team2)
print("-----------------------------------\nSecond Innings")
print("Overs{:10d}|{:10d}Runs")
runs2 ,wicks2 = innings2(team2,team1,runs1)
print("\nTeam 1 Score and Wickets : ", runs1, wicks1)
print("Team 2 Score and Wickets : ", runs2, wicks2)
if(runs1 > runs2):
	print("Team 1 Won!!!\n")
elif(runs1 < runs2):
	print("Team 2 Won!!!\n")
else:
	print("Tie")



'''player = pd.read_csv('step2/player_to_player.csv')
player_prob = pd.DataFrame(columns=['batsman','bowler','0','1','2','3','4','6','notout','balls'])
for i in range(len(player)):
	player_prob.at[i] = [None for n in range(10)]
	player_prob.at[i,'batsman'] = player.at[i,'batsman']	       
	player_prob.at[i,'bowler'] = player.at[i,'bowler']
	player_prob.at[i,'0'] = float(player.at[i,'0'])                            #Finding cumulative probabilities
	player_prob.at[i,'1'] = float(player.at[i,'1']) + float(player.at[i,'0'])
	player_prob.at[i,'2'] = float(player.at[i,'2']) + float(player_prob.at[i,'1'])
	player_prob.at[i,'3'] = float(player.at[i,'3']) + float(player_prob.at[i,'2'])
	player_prob.at[i,'4'] = float(player.at[i,'4']) + float(player_prob.at[i,'3'])
	player_prob.at[i,'6'] = float(player.at[i,'6']) + float(player_prob.at[i,'4'])
	player_prob.at[i,'notout'] = 1 - float(player.at[i,'out'])
	player_prob.at[i,'balls'] = player.at[i,'balls']
	print(i)
player_prob.to_csv('player_cumprob.csv')'''

'''def getruns(batsman,bowler):
	row = player_prob.loc[player_prob['batsman'] == batsman].loc[player_prob['bowler'] == bowler]
	if (row['balls'] >=15):  #if balls played is less than 15 use cluster probabilities
		ret = playerprob(batsman,bowler)
	else:
		ret = clusterprob(bat_clust[batsman],bowl_clust[bowler])
	return ret'''
