# Program build falre list. This program transform the hessi flare list into a workable set of lists in python. 
# The list will use for downloading the necessary data

from scipy.io.idl import readsav 
from datetime import datetime
from datetime import timedelta
import numpy

s = readsav('hsi_limb_list.sav')


date_list  = s['data']['FIELD02'][0]   
stime_list = s['data']['FIELD03'][0]
mtime_list = s['data']['FIELD04'][0]
etime_list = s['data']['FIELD05'][0] 
xpos_list  = s['data']['FIELD10'][0]
ypos_list  = s['data']['FIELD11'][0]
rpos_list  = s['data']['FIELD12'][0]

str = ' '
data = []
skipped = []

oldtime = datetime.strptime('1-Jan-1970 00:00:00', '%d-%b-%Y %H:%M:%S')
d = timedelta(minutes=90) 
# 90 minutes original

for idate, stime,mtime,etime,xpos,ypos,rpos in zip(date_list, stime_list,mtime_list,etime_list,xpos_list,ypos_list,rpos_list):
    tmp0 = datetime.strptime(str.join([idate,stime]), '%d-%b-%Y %H:%M:%S')
    tmp1 = datetime.strptime(str.join([idate,mtime]), '%d-%b-%Y %H:%M:%S')
    tmp2 = datetime.strptime(str.join([idate,etime]), '%d-%b-%Y %H:%M:%S')

    if rpos > 940 and rpos <1055:  #Always check the radial distances limits
        if tmp0.year >= 2010 : 
            if  (tmp0 + d) > oldtime:
                data.append([tmp0,tmp1,tmp2,xpos,ypos,rpos])
            else:
                print 'Date: %s skipped'%tmp0
                skipped.append([tmp0,tmp1,tmp2,xpos,ypos,rpos])
    oldtime = tmp0

data.sort()
skipped.sort()

print len(data),len(skipped)

numpy.save('hsi_wlf_flare_limb_list_limb.npy', data)
