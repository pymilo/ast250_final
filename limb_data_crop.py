import matplotlib.pyplot as plt
import numpy as np
import sunpy.io
from sunpy.map import Map
from sunpy.net import vso
import os
import copy

from datetime import datetime
from datetime import timedelta

# Load numpy list
data_list = np.load('M_X_hsi_goes_flare_list_2013.npy')
d0 = timedelta(minutes=30)
d1 = timedelta(minutes=60)

d = timedelta(minutes=1)
d2 = timedelta(minutes=1)

#directory string and check

dummy = '_'
dummd = '/'
dummt = ':'
dumms = ' '

for i in range(0, len(data_list)):
        # time limits
        init_time = data_list[i][0] - d0
        end_time  = data_list[i][0] + d1

        itime = dumms.join([dummd.join([str(init_time.year),str(init_time.month),str(init_time.day)]),
                dummt.join([str(init_time.hour),str(init_time.minute)])])

#	directory = dummy.join([str(init_time.year),str(init_time.month),str(init_time.day),str(init_time.hour),str(init_time.minute)])
	directory = dummy.join(["%04d"%(init_time.year),
					"%02d"%(init_time.month),
					"%02d"%(init_time.day),
					"%02d"%(init_time.hour),
					"%02d"%(init_time.minute)])

	tmp = '/'
	dbase_dir = tmp.join(['dbase',directory])

	#to be read from the modified flare list
	rhsi_pos = [data_list[i][3],data_list[i][4]]
	hxrange = [rhsi_pos[0]-100, rhsi_pos[0]+100]
	hyrange = [rhsi_pos[1]-100, rhsi_pos[1]+100]

	hxrange.sort()
	hyrange.sort()

	counter =0

	if not os.path.exists('images/%s'%directory):
			print 'directory %s do not exist, creating images directoy and downloading files'%directory
			os.makedirs('images/%s'%directory)

	if not os.path.exists('movies/%s'%directory):
			print 'directory %s do not exist, creating movies directoy and downloading files'%directory
			os.makedirs('movies/%s'%directory)

	if not os.path.exists('fits/%s'%directory):
			print 'directory fits/%s do not exist, creating movies directoy and downloading files'%directory
			os.makedirs('fits/%s'%directory)

	if not os.path.exists('movies/%s/%s.mp4'%(directory,directory)):

		for filename in os.listdir(dbase_dir):
			print 'opening file: %s/%s ... counter = %d'%(dbase_dir,filename,counter)
			#Check file size
			statinfo = os.stat('%s/%s'%(dbase_dir,filename))

			#If file is not of the correct size download again
			if statinfo.st_size != 33563520:
				print 'downloading file %s'%filename

				tmp0 = filename.split('_')
				tmp1 = dumml.join([tmp0[3],tmp0[4],tmp0[5]])
				tmp2 = dummt.join([tmp0[6],tmp0[7],tmp0[8]])

				tmp_tai = dumms.join([tmp1,tmp2])
				 # Open a file
				fo = open("taitoutc.pro", "wb")
				fo.write("x = anytim('%s',/stime) \n"%tmp_tai);

				fo.write("openw,1,'tmp_time.txt' \n");
				fo.write("printf,1,x \n");
				fo.write("close,1\n")
				fo.write("end")
				# Close opend file
				fo.close()

				os.system('./taitoutc.csh')


				f=open('tmp_time.txt','r')
				atmp = f.read()
				f.close()

				nofrac = atmp.split('.')
				itime = datetime.strptime(nofrac[0], '%d-%b-%Y %H:%M:%S') - d
				etime = datetime.strptime(nofrac[0], '%d-%b-%Y %H:%M:%S') + d2

				print itime
				print etime

				# tmp0 = filename.split('_')
				# tmp1 = dumml.join([tmp0[3],tmp0[4],tmp0[5]])
				# tmp2 = dummt.join([tmp0[6],tmp0[7],tmp0[8]])
				# itime = datetime.strptime(dumms.join([tmp1,tmp2]), '%Y-%m-%d %H:%M:%S') - d
				# etime = datetime.strptime(dumms.join([tmp1,tmp2]), '%Y-%m-%d %H:%M:%S') - d1

				os.system("rm -v %s/%s"%(dbase_dir,filename))
				client=vso.VSOClient()
				qr=client.query(vso.attrs.Time(itime, etime), vso.attrs.Instrument('hmi'), 
					vso.attrs.Physobs('intensity'))
				print qr.num_records()
				res=client.get(qr, path='%s/{file}.fits'%dbase_dir).wait() 

				os.system("rm %s/*.0.fits"%dbase_dir)

			pairs = sunpy.io.read_file('%s/%s'%(dbase_dir,filename))

			hmi = sunpy.map.Map('%s/%s'%(dbase_dir,filename))
			hmi.meta['CROTA2'] = hmi.meta['crota2']
			hmi0 = hmi.rotate()
			hmi1 = hmi0.submap(hxrange, hyrange, units='data')

			del hmi

			fig = plt.figure()
			ax =hmi1.plot()

			ff = filename.split('.')
			fig.savefig('images/%s/%s.png'%(directory,ff[0]),format='png')
			plt.close(fig)
			hmi1.save('fits/%s/%s.fits'%(directory,ff[0]))

			#Difference part
			if counter != 0:
				dmap = copy.copy(hmi0)
				dmap.data = hmi0.data - hmi_old.data
				hmi2 = dmap.submap(hxrange, hyrange, units='data')
				del dmap

				fig = plt.figure()
				ax =hmi2.plot()

				fig.savefig('images/%s/diff0_%s.png'%(directory,ff[0]),format='png')
				plt.close(fig)


				fig = plt.figure()
				ax =hmi2.plot(vmin = -70, vmax = 70)

				fig.savefig('images/%s/diff_%s.png'%(directory,ff[0]),format='png')
				plt.close(fig)

		#		hmi2.save('tmp/diff_%s'%filename)

			
			hmi_old = copy.copy(hmi0)
			counter =counter + 1
			del hmi0

		#Make Movies
		os.system("ffmpeg -y -r 15 -pattern_type glob -i 'images/%s/hmi_ic*.png' -c:v libx264 -pix_fmt yuv420p movies/%s/%s.mp4"%(directory,directory,directory))
		os.system("ffmpeg -y -r 15 -pattern_type glob -i 'images/%s/diff_hmi_ic*.png' -c:v libx264 -pix_fmt yuv420p movies/%s/diff_70%s.mp4"%(directory,directory,directory))
		os.system("ffmpeg -y -r 15 -pattern_type glob -i 'images/%s/diff0_hmi_ic*.png' -c:v libx264 -pix_fmt yuv420p movies/%s/diff_%s.mp4"%(directory,directory,directory))

