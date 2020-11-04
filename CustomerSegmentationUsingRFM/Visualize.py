from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import pandas as pd


class Visualize_Cluster:

	@classmethod
	def plot(cls,*df):
		clust0 = pd.read_csv('clust0.csv')
		clust1 = pd.read_csv('clust1.csv')
		clust2 = pd.read_csv('clust2.csv')
		clust3 = pd.read_csv('clust3.csv')
		clust4 = pd.read_csv('clust4.csv')
		clust5 = pd.read_csv('clust5.csv')

		fig = plt.figure()
		ax = fig.add_subplot(111,projection = '3d')
		ax.scatter(clust0['Recency'],clust0['Frequency'],clust0['Monetary'],color = 'Red')
		ax.scatter(clust1['Recency'],clust1['Frequency'],clust1['Monetary'],color = 'Gold')
		ax.scatter(clust2['Recency'],clust2['Frequency'],clust2['Monetary'],color = 'Cyan')
		ax.scatter(clust3['Recency'],clust3['Frequency'],clust3['Monetary'],color = 'Pink')
		ax.scatter(clust4['Recency'],clust4['Frequency'],clust4['Monetary'],color = 'Blue')
		ax.scatter(clust5['Recency'],clust5['Frequency'],clust5['Monetary'],color = 'Green')


		ax.set_xlabel('Recency')
		ax.set_ylabel('Frequency')
		ax.set_zlabel('Monetary')

		plt.show()