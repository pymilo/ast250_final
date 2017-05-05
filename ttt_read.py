
import numpy as np
from urllib2 import urlopen
from StringIO import StringIO
from datetime import datetime
from datetime import timedelta
import numpy


def het_proton_lcurve_range(t1, t2, stereo, tres):

	"""Read RHESSI flare list into numpy array"""

	#RHESSI website
	website = 'http://hesperia.gsfc.nasa.gov/hessidata/dbase/hessi_flare_list.txt'
			
	#read website text
	txt = urlopen(website).read()

	#Get rid of the header and footer of the rhessi flare list
	s = txt.split('\n\n  ')[1]
	ss = s.split('\n\nNotes:')[0].split('\n')

	#create data array
	l = len(ss)
	data = np.zeros((l,),dtype=('a10, a11, a9, a10, a10, i4, i4, i4, a10, i4, i4, i4, i4'))

	#populate data array, where each line is a new event - Does not include Flags
	for line in range(len(ss)):
		sss = filter(None, ss[line].split(' '))
		data[line] = (sss[0], sss[1], sss[2], sss[3], sss[4], sss[5], sss[6], sss[7], sss[8], sss[9], sss[10], sss[11], sss[12])


	return data

data = het_proton_lcurve_range(1,2,3,4)

oldtime = datetime.strptime('1-Jan-1970 00:00:00', '%d-%b-%Y %H:%M:%S')
d = timedelta(minutes=90)

sdata = []
astr = ' '
counter = 0
for i in range(len(data)):
	tmp0 = datetime.strptime(astr.join([data[i][1],data[i][2]]), '%d-%b-%Y %H:%M:%S')
	tmp1 = datetime.strptime(astr.join([data[i][1],data[i][3]]), '%d-%b-%Y %H:%M:%S')
	tmp2 = datetime.strptime(astr.join([data[i][1],data[i][4]]), '%d-%b-%Y %H:%M:%S')
	
	if data[i][11] > 950 and data[i][11] <970. :
		if tmp0.year >= 2011 : 
			ddt = (tmp0 + d) - oldtime
			print ddt.days
			if  ddt.days > 0 :
				if counter != 0 :
					sdata.append([tmp0,tmp1,tmp2,data[i][9],data[i][10],data[i][11],flag])
				flag = 0
				sdata.append([tmp0,tmp1,tmp2,data[i][9],data[i][10],data[i][11],flag])
				oldtime = tmp0
				counter = 0
			else:
				flag = 1 + counter
				counter = counter + 1

for i in range(len(sdata)):
	print sdata[i][0].ctime(),sdata[i][1].ctime(),sdata[i][2].ctime(),sdata[i][3],sdata[i][4],sdata[i][5],sdata[i][6]