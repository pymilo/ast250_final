import numpy as np
import numpy
import os
import sys
import glob

from datetime import datetime
from datetime import timedelta

data_list00 = numpy.load('M_X_hsi_goes_flare_list_2013.npy')
data_list01 = numpy.load('M_X_hsi_goes_flare_list_2013_930.npy')

data_list0 = numpy.concatenate((data_list00,data_list01))

d0 = timedelta(minutes=30)
d1 = timedelta(minutes=60)

data_list = sorted(data_list0, key=lambda data_list0: data_list0[0])

#data_list0 = np.load('M_X_hsi_goes_flare_list_2012_930.npy')
#data_list = sorted(data_list0, key=lambda data_list0: data_list0[0])
#d0 = timedelta(minutes=30)
#d1 = timedelta(minutes=60)

print data_list

#directory string and check

dummy = '_'
dummd = '/'
dummt = ':'
dumms = ' '

for i in range(0, len(data_list)):
#for i in range(42, 43):
        # time limits
    init_time = data_list[i][0] - d0

    itime = dumms.join([dummd.join([str(init_time.year),str(init_time.month),str(init_time.day)]),
                        dummt.join([str(init_time.hour),str(init_time.minute)])])

#	directory = dummy.join([str(init_time.year),str(init_time.month),str(init_time.day),str(init_time.hour),str(init_time.minute)])
    directory = dummy.join(["%04d"%(init_time.year),
    "%02d"%(init_time.month),
    "%02d"%(init_time.day),
    "%02d"%(init_time.hour),
    "%02d"%(init_time.minute)])

    print directory,data_list[i][2],data_list[i][3]
    f1=open('./myfile.pro', 'w+')
#    print "sdo_crop,/new,dir='%s',%f,%f,/diff \n"%(directory,data_list[i][2],data_list[i][3])
    f1.write("sdo_crop_drot_new,/new,dir='%s',xposc=%f,yposc=%f, /plot,/diff \n"%(directory,data_list[i][2],data_list[i][3]))
#    f1.write("sdo_crop_no_drot,/new,dir='%s',xposc=%f,yposc=%f,/plot,/diff \n"%(directory,data_list[i][2],data_list[i][3]))
    #f1.write('end')
    f1.close()
    
    os.system("./myscript")
    
    
