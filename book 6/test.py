import hist , pickle , matplotlib.pyplot as plt,random
from hist import Hist
file = open(r"book 6\data_out.json","rb")
data = pickle.load(file)
random.shuffle(data)
histagram = Hist(hist.axis.Regular(30, 105, 160))
print("ploting...")
histagram.fill(data)


def fit_function(x, a, b, c,):
    background = (a * x) +  (b * x * x) + (c * x * x * x)
    return (background)

fig = plt.figure(figsize=(10, 8))
main_ax_artists, sublot_ax_arists = histagram.plot_ratio(fit_function)

fig = plt.figure(figsize=(10, 8))
main_ax_artists, sublot_ax_arists = histagram.plot_ratio(
    fit_function,
    eb_ecolor="black",
    eb_mfc="black",
    eb_mec="black",
    eb_fmt="o",
    fp_c="red",
    fp_ls="-",
    fp_lw=2,
    fp_alpha=0.8,
)


plt.show()