import numpy as np
import matplotlib
import matplotlib.pylab as plt
import datetime

## Filename
wave = "540" ### centre wavelength
date = "180721" ### YYMMDD
filenum = "001"

filestr = wave+"_"+date+"."+filenum

## pixels (1 indexed)
abs_max_pix = 642
abs_min_pix = 649

### read in files
backfile = "ib"+filestr
raw_backg = np.genfromtxt(backfile, delimiter = '\t', usecols = xrange(2, 1026))
i0file = "i0"+filestr
raw_i0 = np.genfromtxt(i0file, delimiter = '\t', usecols = xrange(2, 1026))
iifile = "ii"+filestr
raw_ii = np.genfromtxt(iifile, delimiter = '\t', usecols = xrange(2,1026))

## sizes
bg_rows = np.shape(raw_backg)[0]
bg_cols = np.shape(raw_backg)[1]

i0_rows = np.shape(raw_i0)[0]
i0_cols = np.shape(raw_i0)[1]

ii_rows = np.shape(raw_ii)[0]
ii_cols = np.shape(raw_ii)[1]

#Initialise
avg_backg = np.zeros((bg_cols))
avg_i0 = np.zeros((i0_cols))
ii_clean = np.zeros((ii_rows,ii_cols))

max_abs = np.zeros((ii_rows))
min_abs = np.zeros((ii_rows))
diff_abs = np.zeros((ii_rows))

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

### Calculate absorption at "peak" and "trough" of I2 absorption spectrum and calculate difference
for i in xrange(0, ii_rows):
    max_abs[i] = ((i0_clean[abs_max_pix-1]/ii_clean[i, abs_max_pix-1]) - 1)
    min_abs[i] = ((i0_clean[abs_min_pix-1]/ii_clean[i, abs_min_pix-1]) - 1)

    diff_abs[i] = max_abs[i] - min_abs[i]


### Read in time column from Ii and convert to usable time data
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


### Plot
fig, ax = plt.subplots(1)
fig.autofmt_xdate()
plt.plot(time_arr, diff_abs)
t_form = matplotlib.dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(t_form)
plt.show()


### Save data
output = np.column_stack((time_arr, diff_abs))
outstr = wave+"_"+date+"_diffabs.txt"
np.savetxt(outstr, output, delimiter = ',', fmt = "%s, %f")
