# This programs download the list of dates to the corresponding directories

from datetime import datetime
from datetime import timedelta
import numpy
import sunpy
from sunpy.net import vso
import os
from pylab import save
from pylab import load
import time

# Load numpy list
data_list = numpy.load('M_X_hsi_goes_flare_list_test.npy')
d0 = timedelta(minutes=30)
d1 = timedelta(minutes=60)


#directory string and check
dummy = '_'
dummd = '/'
dummt = ':'
dumms = ' '

for i in range(0, len(data_list)):
	# time limits
	print(time.localtime())
	init_time = data_list[i][0] - d0
	end_time  = data_list[i][0] + d1

	itime = dumms.join([dummd.join([str(init_time.year),str(init_time.month),str(init_time.day)]),
			    dummt.join([str(init_time.hour),str(init_time.minute)])])
	etime = dumms.join([dummd.join([str(end_time.year),str(end_time.month),str(end_time.day)]),
			    dummt.join([str(end_time.hour),str(end_time.minute)])])
	directory = dummy.join(["%04d"%(init_time.year),
				"%02d"%(init_time.month),
				"%02d"%(init_time.day),
				"%02d"%(init_time.hour),
				"%02d"%(init_time.minute)])

	if not os.path.exists('dbase/%s'%directory):
		print('directory %s do not exist, creating directoy and downloading files'%directory)
		os.makedirs('dbase/%s'%directory)
		# VSO download
		client=vso.VSOClient()
		qr=client.query(vso.attrs.Time(itime, etime), vso.attrs.Instrument('hmi'), vso.attrs.Physobs('intensity'))
		nrec = len(qr)
		save("recnums/%s.txt"%directory, nrec)
		print(nrec)
		res=client.get(qr, path='./tmp/{file}.fits').wait()
		listOfFiles = os.listdir('./tmp')
		for f in listOfFiles:
			os.system ("mv ./tmp/%s ./dbase/%s"%(f,directory))
		save("recnums/%s.txt"%directory, nrec)
	else:
		print("Directory %s exists"%directory)

'''
        #load number of records
	snrec = load("recnums/%s.txt.npy"%directory)
	nfiles = len([name for name in os.listdir("./dbase/%s"%directory)])
	
	if not nfiles == snrec:
		print('Number of files incorrect: downloading files to %s nrec = %d...nfiles = %d'%(directory,snrec,nfiles))
		# VSO download

		client=vso.VSOClient()
                qr=client.query(vso.attrs.Time(itime, etime), vso.attrs.Instrument('hmi'), vso.attrs.Physobs('intensity'))
                nrec = qr.num_records()
                res=client.get(qr, path='./tmp/{file}.fits').wait()
                listOfFiles = os.listdir('./tmp')
                for f in listOfFiles:
                        os.system ("mv ./tmp/%s ./dbase/%s"%(f,directory))

                #Remove .0. files                                                                                     
                filelist = [ f for f in os.listdir("./dbase/%s"%directory) if f.endswith(".0.fits") ]
                if len(filelist) != 0:
                        for f in filelist:
                                os.remove("./dbase/%s/%s"%(directory,f))

print(' ')
print(' ')
print(' ')
print(' ')
print(' ')
print(' ')
print('***************')
print('  Finished!!!')
print('***************')
'''
