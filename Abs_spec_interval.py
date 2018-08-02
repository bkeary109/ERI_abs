###  Average dI/I for a given time interval ###

import numpy as np
import matplotlib
import matplotlib.pylab as plt
import datetime
import sys

### File parameters
wave = "427" ###Wavelength
date = "180724" ### YYMMDD
filenum = "002"


### Error catching ###
if len(sys.argv) != 3:
    sys.exit("Failure. Run with start time and end time as arguments. Format: HH:MM")

##### Time interval to plot spectrum #####
plottime1 = sys.argv[1]   ## format: "HH:MM"
plottime2 = sys.argv[2]   ## format: "HH:MM"

filestr = wave+"_"+date+"."+filenum

### read in files
backfile = "ib"+filestr
raw_backg = np.genfromtxt(backfile, delimiter = '\t', usecols = xrange(2, 1026))
i0file = "i0"+filestr
raw_i0 = np.genfromtxt(i0file, delimiter = '\t', usecols = xrange(2, 1026))
iifile = "ii"+filestr
raw_ii = np.genfromtxt(iifile, delimiter = '\t', usecols = xrange(2,1026))

### Get times
time_list = []
with open(iifile) as f:
    for row in f:
        if row.startswith("#"):
            pass
        else:
            time_list.append(row.split('\t')[1])

time_len = np.shape(time_list)
new_time = []

for i in xrange(0,time_len[0]):
    val = time_list[i]
    x = datetime.datetime.strptime(val, '%H:%M:%S')
    new_time.append(x)

time_arr = np.asarray(new_time)

## sizes
bg_rows = np.shape(raw_backg)[0]
bg_cols = np.shape(raw_backg)[1]

i0_rows = np.shape(raw_i0)[0]
i0_cols = np.shape(raw_i0)[1]

ii_rows = np.shape(raw_ii)[0]
ii_cols = np.shape(raw_ii)[1]

print i0_rows

#Initialise
avg_backg = np.zeros((bg_cols))
avg_i0 = np.zeros((i0_cols))
ii_clean = np.zeros((ii_rows,ii_cols))
abs_vals = np.zeros((ii_rows,ii_cols))

### Average background and I0 and clean I0 and Ii
for n in xrange(1, bg_cols):
    for m in xrange(0, bg_rows):
        avg_backg[n-1] = avg_backg[n-1] + raw_backg[m,n]

avg_backg = avg_backg/bg_rows

for s in xrange(1, i0_cols):
    for t in xrange(0, i0_rows):
        avg_i0[s-1] = avg_i0[s-1] + raw_i0[t,s]

avg_i0 = avg_i0/i0_rows
i0_clean = avg_i0 - avg_backg
for a in xrange(0, ii_rows):
    ii_clean[a] = raw_ii[a] - avg_backg


### Calculate absorption
for m in xrange(0,ii_rows):
    for n in xrange(0, ii_cols):
        abs_vals[m,n] = (i0_clean[n]/ii_clean[m,n])-1

### Find spectrum at given time
for i in xrange(0, ii_rows):
    if time_arr[i].strftime("%H:%M") == plottime1:
        specpoint1 = i
        print time_arr[i]
        break
for j in xrange(0, ii_rows):
    if time_arr[j].strftime("%H:%M") == plottime2:
	specpoint2 = j
	print time_arr[j]
	break

avg_spec = np.zeros((1, ii_cols))
for l in xrange(0, ii_cols):
    for k in xrange(specpoint1, specpoint2):
	avg_spec[0, l] = avg_spec[0, l] + abs_vals[k-specpoint1, l]

avg_factor = specpoint2-specpoint1
avg_spec = avg_spec/avg_factor

print avg_factor
print "Save spectrum (Y/N)?"

sys.stdout.flush()

### Plot
plt.title("Average Absorption from " + plottime1 + " to " +plottime2)
plt.plot(xrange(1,1025), np.transpose(avg_spec))
plt.show()

#print "continue"
save = raw_input()

### Write to file
if save == "Y" or save == "y":
    pixels = np.zeros((1024))
    for p in xrange(1,1025):
        pixels[p-1] = p
    output = np.column_stack((pixels, np.transpose(avg_spec)))
    outtime1 = time_arr[specpoint1].strftime("%H-%M")
    outtime2 = time_arr[specpoint2].strftime("%H-%M")
    outfile = wave+"_"+date+"_t"+outtime1+"--"+outtime2+".txt"

    np.savetxt(outfile, output, delimiter=',')
    print "\nSpectrum averaged from " + plottime1 + " to " + plottime2 + " saved\n"
else:
    print "\nSpectrum not saved\n"
