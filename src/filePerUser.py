# importing bandicoot lib
import bandicoot as bd

import datetime as dt
import os
import re
import json
import csv


# 1: incoming, 2: outgoing, 3: missed call/text

def compileAll(row):
	
	with open('records/records.csv','a') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
    		for i in row:
			writer.writerow(i)	
	
def findAntenna(num,i):
		
	try:
		os.chdir('../'+str(i)+'_probedata')
		with open("(u'edu.mit.media.funf.probe.builtin.CellTowerProbe',).json",'r') as file2:
			data2=json.load(file2) #Contains antenna ids	

		minD=1000000000
		finalAntenna=0
		
		for k in data2:
			
			try:
				antenna_id=re.search("{\"cid\":(.+?),\"lac",k[1]).group(1)
				#print k[2], "Antenna id", antenna_id
				timestamp=dt.datetime.fromtimestamp(k[2]-50000).strftime("%Y-%m-%d %H:%M:%S") #IST
			
				#print antenna_id,timestamp
				
				if num>k[2]-50000:
					#print 'yes', antenna_id, num,datetime, k[2]-50000, timestamp,k[2],dt.datetime.fromtimestamp(k[2]).strftime("%Y-%m-%d %H:%M:%S"),num-k[2]+50000
					if minD>(num-k[2]+50000):
						minD=num-k[2]+50000
						finalAntenna=antenna_id
						#print 'minD',minD
					#print minD, antenna_id
				
			except Exception as e:
				pass
		
	except Exception as e:
		pass

	finally:
		if minD<1000000000:
			
			return finalAntenna
		
def callSorter(i):
	
	try:
		os.chdir('../'+str(i)+'_probedata')
		with open("(u'edu.mit.media.funf.probe.builtin.CallLogProbe',).json",'r') as file:
			data=json.load(file)

		row=[]
		for j in data:	
			interaction='Call'

			a=re.search("\"type\":(.+?)}",j[1]).group(1)
			d=['In','Out','Missed']
			direction=d[int(a)-1]
			#print 'Direction', direction
			
			found=re.search("number\":\"{\\\(.+?)\\\"}\",\"numberlabel",j[1]).group(1)
			correspondent_id=re.sub(r'[\\,:,"]','',re.split("ONE_WAY_HASH", found, maxsplit=2)[1])
			if correspondent_id!='':
				#print correspondent_id
				pass			
			else:
				correspondent_id='NONE'	
				#print 'Correspondent_Id',correspondent_id
			
			datetime=dt.datetime.fromtimestamp(j[2]).strftime("%Y-%m-%d %H:%M:%S") #IST
			#print datetime

			duration=re.search("duration\":(.+?),", j[1]).group(1)
			#print 'Duration',duration
			

			#Finding Antenna Id
			antenna=findAntenna(j[2],i)
			
			setA=[interaction,direction,correspondent_id,datetime,str(duration),antenna]	
			#if correspondent_id=='NONE':
			#	print setA				
			row.append(setA)
		compileAll(row)
	except Exception as e:
		pass


def textSorter(i):
	try:
		os.chdir('../'+str(i)+'_probedata')
		with open("(u'edu.mit.media.funf.probe.builtin.SmsProbe',).json",'r') as file:
			data=json.load(file)
		row=[]
		row.append(['interaction','direction','correspondent_id','datetime','call_duration','antenna_id'])
		for j in data:	
			interaction='Text'

			a=re.search("\"type\":(.+?)}",j[1]).group(1)
			d=['In','Out']
			direction=d[int(a)-1]
			#print 'Direction', direction

			found=re.search("address\":\"{\\\(.+?)\\\"}\",\"body",j[1]).group(1)
			correspondent_id=re.sub(r'[\\,:,"]','',re.split("ONE_WAY_HASH", found, maxsplit=2)[1])
			#print 'Correspondent_Id',found
			if correspondent_id!='':
				#print correspondent_id
				pass			
			else:
				correspondent_id='NONE'	
				#print 'Correspondent_Id',correspondent_id

			datetime=dt.datetime.fromtimestamp(j[2]).strftime("%Y-%m-%d %H:%M:%S") #IST
			#print datetime

			duration='0'
	
			#Finding Antenna Id
			antenna=findAntenna(j[2],i)	
			
			setA=[interaction,direction,correspondent_id,datetime,str(duration),antenna]	
			#if correspondent_id=='NONE':
			#	print setA				
			row.append(setA)
			try:
    				os.remove('records.csv')
			except OSError:
    				pass
		compileAll(row)
			
	except Exception as e:
		pass

def compileLoc(row):
	with open('antennas.csv','wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
    		for i in row:
			writer.writerow(i)	

def locationSorter(i):
	try:
		os.chdir('../'+str(i)+'_probedata')
		with open("(u'edu.mit.media.funf.probe.builtin.LocationProbe',).json",'r') as file:
			data=json.load(file)
		row=[]
		row.append(['place_id','latitude','longitude'])

		for j in data:	
			found=re.search("mIsFromMockProvider\":false,(.+?)\"mProvider\":", j[1]).group(1)
			latitude=re.search("mLatitude\":(.+?),\"mLongitude\":",found).group(1)
			longitude=re.search("mLongitude\":(.+?),",found).group(1)			
			
			#datetime=dt.datetime.fromtimestamp(j[2]).strftime("%Y-%m-%d %H:%M:%S") #IST
			#print datetime

			#Finding Antenna Id
			antenna=findAntenna(j[2],i)	
			row.append([antenna,latitude,longitude])
		compileLoc(row)
			
	except Exception as e:
		pass
	
def main():
	for i in range(1,13):
		print 'Folder ',i		
		textSorter(i)
		callSorter(i)
		#csvSorter()
		locationSorter(i)
