import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import  MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


class Preprocessing:

	def fix_data(self,retail):
		retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'],format='%m/%d/%Y %H:%M')



class RFMAnalysis:

	def extract_day(self,retail):
		retail['InvoiceDay'] = retail.InvoiceDate.apply(lambda x: dt.datetime(x.year, x.month, x.day))

	def min_max_day(self,retail):
		# print the time period
		print('Min : {}\nMax : {}'.format(min(retail.InvoiceDay), max(retail.InvoiceDay)))
	
	
	def rfm_111(self,rfm):
		print(rfm.loc[rfm['RFM_Segment'] == '111',['Recency','Frequency','Monetary']].head())

	def rfm_444(self,rfm):
		print(rfm.loc[rfm['RFM_Segment'] == '444',['Recency','Frequency','Monetary']].head())


	def calculate_rfm(self,retail):

		pin_date = max(retail.InvoiceDay) + dt.timedelta(1)

		retail['TotalSum'] = retail.Quantity * retail.UnitPrice


		
		# calculate RFM values
		rfm_grouped = retail.groupby('CustomerID').agg({'InvoiceDate' : lambda x: (pin_date - x.max()).days,'InvoiceNo' : 'count', 'TotalSum' : 'sum'})
		

		

		# rename the columns
		rfm_grouped.rename(columns = {'InvoiceDate' : 'Recency','InvoiceNo' : 'Frequency','TotalSum' : 'Monetary'}, inplace = True)
		rfm_grouped.Recency = rfm_grouped.Recency.astype(int)		
		return rfm_grouped



	def rfm_score(self,rfm):


		# create labels and assign them to tree percentile groups 
		r_labels = range(4, 0, -1)
		r_groups = pd.qcut(rfm.Recency, q = 4, labels = r_labels)
		f_labels = range(1, 5)
		f_groups = pd.qcut(rfm.Frequency, q = 4, labels = f_labels)
		m_labels = range(1, 5)
		m_groups = pd.qcut(rfm.Monetary, q = 4, labels = m_labels)


		# make a new column for group labels
		rfm['R'] = r_groups.values
		rfm['F'] = f_groups.values
		rfm['M'] = m_groups.values
		# sum up the three columns
		rfm['RFM_Segment'] = rfm.apply(lambda x: str(x['R']) + str(x['F']) + str(x['M']), axis = 1)
		rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis = 1)


	def assign_labels(self,rfm):

		# assign labels from total score
		score_labels = ['Green', 'Bronze', 'Silver', 'Gold']
		score_groups = pd.qcut(rfm.RFM_Score, q = 4, labels = score_labels)
		rfm['RFM_Level'] = score_groups.values




class K_Means:

	def preprocesser(self,rfm):


		def neg_to_zero(x):
			if x <= 0:
				return 1
			else:
				return x
		# apply the function to Recency and MonetaryValue column 
		rfm['Recency'] = [neg_to_zero(x) for x in rfm.Recency]
		rfm['Monetary'] = [neg_to_zero(x) for x in rfm.Monetary]

		rfm_log = rfm[['Recency', 'Frequency', 'Monetary']].apply(np.log, axis = 1).round(3)

		
		# scale the data
		scaler = MinMaxScaler()
		rfm_scaled = scaler.fit_transform(rfm_log)
		# transform into a dataframe
		rfm_scaled = pd.DataFrame(rfm_scaled, index = rfm.index, columns = rfm_log.columns)
		rfm_scaled['Recency'] = 1-rfm_scaled['Recency']

		return rfm_scaled


	def elbow_plot(self,rfm_scaled):

		# the Elbow method
		wcss = {}
		for k in range(1, 20):
			kmeans = KMeans(n_clusters= k, init= 'k-means++', max_iter= 300,random_state = 0)
			kmeans.fit(rfm_scaled)
			wcss[k] = kmeans.inertia_
		# plot the WCSS values
		sns.pointplot(x = list(wcss.keys()), y = list(wcss.values()))
		plt.xlabel('K Numbers')
		plt.ylabel('WCSS')
		plt.show()



	def make_clusters(self,rfm_scaled,rfm):

		clus = KMeans(n_clusters= 6, init= 'k-means++', max_iter= 300,random_state = 0)
		clus.fit(rfm_scaled)
		# Assign the clusters to datamart
		rfm['K_Cluster'] = clus.labels_








