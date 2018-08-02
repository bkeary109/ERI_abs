import numpy as np
import matplotlib
import matplotlib.pylab as plt
import datetime
import sys

### File parameters
wave = "660" ###Wavelength
date = "180725" ### YYMMDD
filenum = "001"

filestr = wave+"_"+date+"."+filenum

## pixels (1 indexed)
abs_pix = 109

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

#Initialise
avg_backg = np.zeros((bg_cols))
avg_i0 = np.zeros((i0_cols))
ii_clean = np.zeros((ii_rows,ii_cols))

pix_abs = np.zeros((ii_rows))

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

### Calculate absorption at specified pixel
for i in xrange(0, ii_rows):
    pix_abs[i] = ((i0_clean[abs_pix-1]/ii_clean[i, abs_pix-1]) - 1)


print "Save spectrum (Y/N)?"
sys.stdout.flush()

### Plot
fig, ax = plt.subplots(1)
fig.autofmt_xdate()
plt.plot(time_arr, pix_abs)
t_form = matplotlib.dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(t_form)
plt.show()

save = raw_input()
outtime = []
for elem in time_arr:
    outtime.append(elem.strftime('%H:%M:%S'))

out_time = np.asarray(outtime)

### Write to file
if save == "Y" or save == "y":
    pixstr = str(abs_pix)
    output = np.column_stack((out_time, pix_abs))
    outstr = wave+"_"+date+"_pix"+pixstr+"_abs.txt"
    np.savetxt(outstr, output, delimiter = ',', fmt = "%s, %s")
    print "\nAbsorption at pixel %d saved" %abs_pix
else:
    print "\nData not saved"
