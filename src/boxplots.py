import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pandas
import re
import statistics

# Functions to plot from Student Data

def read_data(path):
	"""function that reads data for plotting out of a .csv"""
	
	df = (pandas.read_csv(path))
	
	#reading data from relevant columns
	val_df = df.pop('STUDENT_VALS')
	years = df["YEAR"].tolist()

	#converting year_values to strings
	years_str = []
	for year in years:

		years_str.append(str(year))
	

	#convertings strings in val_df to actual lists
	data = []

	for data_point in val_df:
		data_point=data_point.replace("[","").replace("]","")
		
		values = []
		for value_str in data_point.split(","):
			values.append(float(value_str))

		data.append(values)


	return data, years, df

def get_min_max(arrays):
	"""function that returns the minimum and maximum for arrays within an array"""
	min_array = []
	max_array = []
	for a in arrays:
		min_array.append(min(a))
		max_array.append(max(a))
		
	minimum = min(min_array)
	maximum = max(max_array)

	return minimum, maximum


def boxplot(yax,xax,title, out_path):
	"""function that creates a boxplot and trendline for entered data and saves it"""
	
	# extracting minimum and maximum and getting the upper bound
	minimum, maximum = get_min_max(yax)
	
	upper_bound = maximum * 1.1
	lower_bound = minimum * 0.9

	# calculating trendline
	medians = []
	for array in yax:
		medians.append(statistics.median(array))
	
	
	theta = np.polyfit(xax, medians, 1)

	y_line = []
	for year in xax:

		y_line.append(theta[1] + theta[0] * year)
		
	#creating the plots
	fig1, ax1 = plt.subplots(figsize=(15,10))
	ax1.set_ylabel(title)
	ax1.set_xlabel("YEAR")
	ax1.boxplot(yax,labels=xax, notch=True, showfliers=False)
	#ax1.set(ylim=(lower_bound, upper_bound))
	lower_bound, upper_bound = ax1.get_ylim()
	fig1.savefig(out_path+'_plot.png', transparent=False, dpi=100, bbox_inches="tight")

	fig2, ax2 = plt.subplots(figsize=(15,10))
	ax2.set_ylabel(title)
	ax2.set_xlabel("YEAR")
	ax2.scatter(xax, medians)
	ax2.plot(xax, y_line, 'r')
	ax2.set(ylim=(lower_bound, upper_bound))
	fig2.savefig(out_path+'_trend.png', transparent=False, dpi=100, bbox_inches="tight")
	plt.close('all')




# Functions to plot Zeit/Express data

def read_data_exze(path):

	"""function that reads data for plotting out of a .csv"""



	df = (pandas.read_csv(path))
	
	#reading data from relevant columns
	val_df = df.pop('ALL_VALS')
	years = df["YEAR"].tolist()

	#converting year_values to strings
	years_str = []
	for year in years:

		years_str.append(str(year))
	

	#convertings strings in val_df to actual lists
	data = []

	for data_point in val_df:
		data_point=data_point.replace("[","").replace("]","")
		
		values = []
		for value_str in data_point.split(","):
			values.append(float(value_str))

		data.append(values)


	return data, years, df
def boxplot_exze(yax,xax,title, out_path):
	"""function that creates a boxplot and trendline for entered data and saves it"""


	fig, ax = plt.subplots()
	ax.set_ylabel(title)
	ax.set_xlabel("NEWSPAPER")
	ax.boxplot(yax,labels=['EXPRESS','ZEIT'],notch=True, showfliers=True)

	fig.savefig(out_path, transparent=False, dpi=300, bbox_inches="tight")
	plt.close()
	# tabulate(xax, yax, title)

# Functions to plot Perplexity data

def read_data_ppl(path):
	"""function that reads data for plotting out of a .csv"""

	df = pandas.read_csv(path)

	# reading data from relevant columns
	val_pplze = df["all_ppl_ZEIT"]
	val_pplex = df["all_ppl_Express"]

	years = df["YEAR"]
	

	# creating plottable lists
	values = []
	year_labels = []
	
	for index in range(len(years)):

		values.append(val_pplex[index]) 
		values.append(val_pplze[index])
		
		year_labels.append(str(years[index])+'\nExpress')
		year_labels.append(str(years[index])+'\nZeit')
		

	data = []

	for data_point in values:
		data_point=data_point.replace("[","").replace("]","")
		
		values = []
		for value_str in data_point.split(","):
			values.append(float(value_str))

		data.append(values)


	return data, year_labels

def boxplot_ppl(yax,xax,title, out_path):
	"""function that creates the boxplots"""
		

	fig, ax = plt.subplots(figsize=(15,5))
	ax.set_ylabel(title)
	ax.set_xlabel("YEAR")
	bplot = ax.boxplot(yax,labels=xax, notch=True, showfliers=False, patch_artist=True)

	colors = []
	code = ['red', 'blue']
	for i in range(len(bplot['boxes'])):
		colors.extend(code)

	for patch, color in zip(bplot['boxes'], colors):
		patch.set_facecolor(color)

	fig.savefig(out_path, transparent=False, dpi=200, bbox_inches="tight")
	plt.close()

	# tabulate(xax, yax, title)


# def tabulate(row,col, filename):

# 	if os.path.isdir("./tables") is False:

# 		os.makedirs("./tables")

# 	table_data = pandas.DataFrame()

# 	table_data["YEAR"] = row
# 	medians=[]

# 	for i in range(len(col)):
# 		medians.append(statistics.median(col[i]))
# 	table_data["MEDIAN"] = medians
	

# 	table_data.to_csv('./tables'+filename+'.csv')

def tabulate(df, values, title):
	median = []
	mean = []

	for index in range(len(values)):

		median.append(statistics.median(values[index]))
		mean.append(statistics.mean(values[index]))

	df['MEAN'] = mean
	df['MEDIAN'] = median

	print(df)


def read_data_exze_new(path):
	"""function that reads data for plotting out of a .csv"""
	
	df = (pandas.read_csv(path))
	
	#reading data from relevant columns
	val_df = df["ALL_VALS"]
	years = df["FILENAME"].tolist()


	#convertings strings in val_df to actual lists
	data = []

	for data_point in val_df:
		data_point=data_point.replace("[","").replace("]","")
		
		values = []
		for value_str in data_point.split(","):
			values.append(float(value_str))

		data.append(values)

	return data, years

def boxplot_exze_new(yax,xax,title, out_path):
	"""function that creates a boxplot and trendline for entered data and saves it"""

	# extracting minimum and maximum and getting the upper bound
	minimum, maximum = get_min_max(yax)

	upper_bound = maximum * 1.1
	

	if 'express' in xax[0]:
		labeling1 = ['Express', 'Zeit']
	else:
		labeling1 = labeling1[::-1]

	#creating the plots
	fig, ax = plt.subplots()
	ax.set_ylabel(title)
	ax.set_xlabel("NEWSPAPER")
	bplot = ax.boxplot(yax,labels=labeling1,notch=True, showfliers=False, patch_artist=True)
	
	colors = []
	code = ['red', 'blue']
	for i in range(len(bplot['boxes'])):
		colors.extend(code)
	for patch, color in zip(bplot['boxes'], colors):
		patch.set_facecolor(color)

	fig.savefig(out_path, transparent=False, dpi=200, bbox_inches="tight")
	plt.close()




