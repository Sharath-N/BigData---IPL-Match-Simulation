import pandas as pd
 #'BatName','BowlName', '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7+','clustNo'
#Eliminate rows where batsman name != Bowler name
#For every clustNo find avg.
cpairs = pd.read_csv('player_to_player.csv')
del cpairs['batsman']
del cpairs['bowler']

final = cpairs.groupby(['batclustno','bowlclustno']).mean()   #Find average of probabilities by grouping by bat cluster no and 
#final = final.groupby().mean()					#bowler cluster number
final.to_csv('clust_to_clust.csv')
