import numpy as np
import matplotlib
import matplotlib.pylab as plt
import datetime

smps_file = "2018_07_27_12_23_36_smps.txt"
outstr = smps_file[0:17] + "particles.txt"

N_part = np.genfromtxt(smps_file, delimiter = '\t', skip_header = 26, usecols = 221)

#Take times from file and convert to datetime.datetime array
time_list = []
num_row = 0
with open(smps_file) as f:
    for row in f:
        if num_row < 26:
            pass
        else:
            time_list.append(row.split('\t')[2])
        num_row = num_row + 1

time_len = np.shape(time_list)
new_time = []

for i in xrange(0,time_len[0]):
    val = time_list[i]
    x = datetime.datetime.strptime(val, '%H:%M:%S')
    new_time.append(x)

time_arr = np.asarray(new_time)

fig, ax = plt.subplots(1)
fig.autofmt_xdate()
plt.plot(time_arr, N_part)
t_form = matplotlib.dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(t_form)
plt.show()

### Save data
outtime = []
for elem in time_arr:
    outtime.append(elem.strftime('%H:%M'))
out_time = np.asarray(outtime)
output = np.column_stack((out_time, N_part))
np.savetxt(outstr, output, delimiter = ',', fmt = "%s, %s")

