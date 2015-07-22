# to calculate metrics, perform factor analysis, and generate visualizations.
import sys
sys.path.append("../")

import bandicoot as bc
import csv
import glob
import os

#Metrics, FA, Tensor, Visualization


def metrics():
	records_path = 'records/'
	antenna_file = 'antennas.csv'

	indicators = []
	for f in glob.glob(records_path + '*.csv'):
	    user_id = os.path.basename(f)[:-4]

	    try:
		B = bc.read_csv(user_id, records_path, antenna_file, describe=False)
		metrics_dict = bc.utils.all(B)
	    except Exception as e:
		metrics_dict = {'name': user_id, 'error': True}

	    indicators.append(metrics_dict)

	bc.io.to_csv(indicators, 'bandicoot_indicators_full.csv')

#def FA():
#def tensor():
#def visualizations():	
