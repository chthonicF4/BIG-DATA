import numpy as np, matplotlib , uproot ,hist , matplotlib.pyplot as plt
from hist import Hist

file = uproot.open("BIG DATA.root")
jet_n = file["mini"]["jet_n"].array(library="np")

min_jet , max_jet = np.min(jet_n) , np.max(jet_n)
print(f"min:{min_jet} max:{max_jet} len:{len(jet_n)}")

histagram = Hist(hist.axis.Regular(max_jet-min_jet,min_jet-0.5,max_jet-0.5),label="jets")
histagram.fill(jet_n)
histagram.plot()
plt.title("jets")
plt.show()



