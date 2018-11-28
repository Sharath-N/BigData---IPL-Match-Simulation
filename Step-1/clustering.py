from pyspark.sql import SparkSession
from pyspark.ml.feature import StandardScaler
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

spark = SparkSession.builder.appName('cricket').getOrCreate()

bat_fp = spark.read.csv('/Project/Input/batsmen2016.csv', header=True, inferSchema=True)
bowl_fp = spark.read.csv('/Project/Input/bowler2016.csv', header=True, inferSchema=True)

bat_cols = ['Ave','SR']
bowl_cols = ['Econ', 'SR']

#bat_fp.printSchema()#bat_fp.show(3)	

def clustering(fp, cols):
	assembler = VectorAssembler(inputCols=cols, outputCol='features')
	assembled_data = assembler.transform(fp)
	scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures')
	print('dkks' scaler)
	#scaler.show()
	scaler_model = scaler.fit(assembled_data)
	scaled_data = scaler_model.transform(assembled_data)

	#scaled_data.printSchema()
	#scaled_data.show(4)
	#scaled_data.select('scaledFeatures').show()

	k_means_3 = KMeans(featuresCol='scaledFeatures', k=10) #clusters = KMeans(fp, 5, maxIterations=10, initializationMode="random")#clusters.show()
	model_k3 = k_means_3.fit(scaled_data)
	model_k3_data = model_k3.transform(scaled_data)
	#details = model_k3_data
	#model_k3_data.groupBy('prediction').count().show()
	#details.show(50)
	return model_k3_data

bat_det = clustering(bat_fp, bat_cols)
bowl_det = clustering(bowl_fp, bowl_cols)

print("\n~~~~~~~~~~~~~~~~~~~ BATSMEN CLUSTER Details ~~~~~~~~~~~~~~~~~~~\n")
bat_det.show(50)
bat_det.groupBy('prediction').count().show()

print("\n~~~~~~~~~~~~~~~~~~~ BOWLER CLUSTER Details ~~~~~~~~~~~~~~~~~~~\n")
bowl_det.show(50)
bowl_det.groupBy('prediction').count().show()
