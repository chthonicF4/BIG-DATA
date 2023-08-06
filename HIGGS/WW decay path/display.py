import hist , pickle , matplotlib.pyplot as plt,random
from hist import Hist

h_bgs = Hist(hist.axis.Regular(50, 60, 300, label = "Transverse mass m_{T}"))
h_dat = Hist(hist.axis.Regular(50, 60, 300, label = "Transverse mass m_{T}"))

bgs = open(r"mc_data_out.json","rb")
dat = open(r"DATA_OUT.json","rb")

bgs = pickle.load(bgs)
dat = pickle.load(dat)

for event,weight in bgs : h_bgs.fill(event,weight=weight)
for event,weight in dat : h_dat.fill(event,weight=weight)

h_dat.plot(histtype = "fill")
plt.show()

h_bgs.plot(histtype = "fill")
plt.show()
h_bgs.sum()

h_dat.plot(histtype = "fill")
h_bgs.plot(histtype = "fill")

plt.show()

h_diff = h_dat - h_bgs

h_diff.plot(histtype = "fill")
plt.show()