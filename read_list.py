import numpy as np
import datetime
import copy

x = np.genfromtxt("test_dataset_test.dat", dtype='str')

fmt = '%d-%b-%Y %H:%M:%S'

list_dataset = []

for i in range(0,len(x)):
	d1 = datetime.datetime.strptime(" ".join([x[i][0],x[i][1]]), fmt)
	d2 = datetime.datetime.strptime(" ".join([x[i][2],x[i][3]]), fmt)
	list_dataset.append([d1,d2,x[i][4], x[i][5], x[i][6], x[i][7]])
#	print d1.isoformat(),d2.isoformat(),x[i][4], x[i][5], x[i][6], x[i][7]

new_list_dataset = [] #copy.copy(list_dataset)
counter = 0 
flag=0
for j in range(1,len(list_dataset)):
	if list_dataset[j][5][0] == 'M' or list_dataset[j][5][0] == 'X':
#	if j == 0:
#		flag = 0
		counter = j 
#	else:
		if list_dataset[j][5] == list_dataset[j-1][5]:
			#print flag
			dy = abs(list_dataset[j][3] - list_dataset[j-1][3])
			dt = round((list_dataset[j][1] - list_dataset[j-1][0]).seconds/60.)
			#print list_dataset[j][1] ,list_dataset[j-1][0],dt,dy

			if np.logical_and(dt < 45., dy < 25.):
				flag = 1
			elif np.logical_and(dt >= 45., dy >= 25.):
				print(list_dataset[j][1].isoformat() ,list_dataset[j-1][0].isoformat(),dt,dy)

				flag = 0
				counter = j
			else:
				continue
		else:
			flag = 0
			counter = j
	else:
		flag=-1
	if flag != -1:
		new_list_dataset.append([ j, list_dataset[j][0], list_dataset[j][1],
			list_dataset[j][2],list_dataset[j][3],list_dataset[j][4],list_dataset[j][5], flag])

final_list = []
icount = 0
for k in range(0,len(new_list_dataset)):
#	print(k,icount,new_list_dataset[k][0],new_list_dataset[k][1].isoformat(),new_list_dataset[k][2].isoformat(),new_list_dataset[k][3],new_list_dataset[k][4],new_list_dataset[k][5],new_list_dataset[k][6],new_list_dataset[k][7])

	if new_list_dataset[k][7] != 0:
		final_list[icount-1][1] = new_list_dataset[k][2]
	else:
		final_list.append([new_list_dataset[k][1],new_list_dataset[k][2],new_list_dataset[k][3],
			new_list_dataset[k][4],new_list_dataset[k][5],new_list_dataset[k][6]])
		icount = icount+1

np.save('M_X_hsi_goes_flare_list_test.npy',final_list)
