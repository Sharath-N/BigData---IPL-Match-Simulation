# BIG DATA - UE16CS313 - PES University

## BigData FinalProject - IPL-Match-Simulation
Simulating the IPL matches with the help of clustering and desicion tree by using the past IPL statistics of players.

### Introduction 
 
IPL match analysis using that data from all the IPL matches from the beginning till date. Our main motive is to predict the score and the match. Here we use two methods to predict the ball-by-ball score :
1. Clustering Method choosing a random probability
2. Decision Tree Model (Teaching the tree with the recent data)

---
### Software Dependencies
* Apache Hadoop- HDFS
* Apache Spark
* Python 3 & Python 2
* PySpark

---
#### ALGORITHM/DESIGN 
 
* *Step 1*:  
The main dataset that we used for prediction was downloaded from https://cricsheet.org/  .
We observed that many batsman-bowler combinations did not occur in the dataset which would cause inaccuracies during prediction. In order to face this situation, we performed clustering to group the batsmen and bowlers using their  statistics provided in the dataset. Hence when we encounter an unfaced combination, we predict the outcome based on the cluster they belong to. 
This involved collecting the batting-averages and bowling-averages of all the players(i.e., the player profile) in IPL from 2008-2017. We wrote a web-scraping code in Python using BeautifulSoup for this purpose. The data was cleaned to meet our requirements and written to a csv file for easy handling. This csv file was loaded into HDFS. 
Next, we wrote a python code for clustering batsmen and bowlers using PySpark MLLIB. The clustering was done using the K-Means algorithm. To optimize the value of k (the number of clusters), an elbow plot was constructed for different values of k ranging from 1 to 40. The visualization yielded an optimal value of 6 for batsmen and value of 5 for bowler.
The parameters used for clustering batsman – Runs, Strike Rate, Average, Number of 4s,6s and 50s
The parameters used for clustering bowlers – Wickets, Economy, Average, Strike Rate

---

* *Step 2*: 
Once the clusters were obtained, we calculated cluster vs cluster statistics using the main dataset which had ball by ball outcome of all matches from 2008-2017. This was done by maintaining a dictionary of batsmen cluster vs bowler cluster parameter totals(0s,1s,2s,3s,4s,6s,wickets). Every time a new combination was encountered, we found the batsman cluster number and the bowler cluster number and added the parameters to the corresponding cluster combination. Finally probabilities of scoring 0s,1s,2s,3s,4s,6s,wickets were obtained for every cluster combination by dividing by the total number of balls.  
A summary statistics file is also generated for every batsman-bowler combination encountered in the main dataset, which contains the probabilities of scoring 
0s,1s,2s,3s,4s,6s and wickets, when that particular combination face each other. 
We wrote a python code to simulate an entire IPL match using ball by ball prediction. To predict the outcome of a ball, we searched for the batsman-bowler combination in the summary statistics file. If not found, or is the batsman had faces less than 15 balls from that bowler we predicted the clusters for the combination and obtained the probabilities for the particular cluster combination. A list of cumulative probabilities is constructed from the probabilities obtained. A random is generated and the outcome is decided based on the range of cumulative probabilities in which it falls. The outcome could be 0,1,2,3,4,6 or a wicket. This is repeated for all balls until 20 overs are up or there are no wickets left. An additional way of a wicket falling is also added. 
We write the outcome of every ball into a CSV file. We simulated 10 matches and calculated the averages. 
---
* *Step 3*: 
Here then we followed the method of using the decision trees. The outcome of the match was predicted using the decision trees.  
Using the phase 2 statistics we use the data and we perform to predict the score again ball by ball.
Using the Spark MLLIB which provides functions to train and construct Decision Tree models. 
 We trained a decision tree model, with the following parameters: 
Batting Average, Batting Strike Rate, Bowling Average, Bowling Economy, Bowling Strike Rate, No of balls (represented with the overs), Innings and finally the Runs. 
This is trained into the regression tree and thus is later used to predict the possible outcomes for the particular match.
Thus we simulate the match give and predict on the basis of the trained decision tree. 
 ---
#### EXPERIMENTAL RESULTS 
 
For clustering –  
Accuracy  : 75.21% 
Error : 24.79% 

For Decision trees(using Regression) –  
Accuracy  : 82.89% 
Error : 17.11% 

---

#### Our Squad:
* SHASHANK S SHETTAR
* SHARATH N
* SHASHI KUMAR JUTOOR
* SACHIN S
