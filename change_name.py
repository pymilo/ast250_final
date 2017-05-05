import numpy
import os


dl = os.listdir('dbase')

for counter,idir in enumerate(dl):
	if counter !=0:
		sstr = "_"
		odir = idir.split('_')
		ndir = sstr.join(["%04d"%(float(odir[0])),
			"%02d"%(float(odir[1])),
			"%02d"%(float(odir[2])),
			"%02d"%(float(odir[3])),
			"%02d"%(float(odir[4]))])

		os.system ("mv ./dbase/%s ./dbase/%s"%(idir,ndir))
		print "mv ./dbase/%s ./dbase/%s"%(idir,ndir)


