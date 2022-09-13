from argparse import ArgumentParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

parser = ArgumentParser()

parser.add_argument('--theme',
                    default='light',
                    nargs='?',
                    choices=['light', 'dark'],
                    help="""The theme for the plots. Choose from 'light' and 'dark'
                    \n(default: %(default)s)
                    """
)

args = parser.parse_args()

if args.theme == 'dark':
    plt.style.use('plots/darkmode.mplstyle')

surv = pd.read_csv("./plots/data/survivor/survivor_tailcuts_MST_MST_NectarCam.csv")
combined = pd.read_csv("./plots/data/combined_table.csv")

tab = combined.copy()
tab = tab[["ratio_tail", "index_tail"]].dropna()
eff = np.array(tab["ratio_tail"])

surv.insert(0, "eff", eff)

print(surv)

fig, (ax, ax2) = plt.subplots(2,1, figsize=(5,5), constrained_layout=True, sharex=True, dpi=300)

ax.plot(surv["eff"], surv["selected_signal"], "o:", label=r"$> 0 \,\mathrm{p.e.}$")
ax.plot(surv["eff"], surv["selected_signal_g1"], "v:", label=r"$> 1 \,\mathrm{p.e.}$")
ax.plot(surv["eff"], surv["selected_signal_g2"], "^:", label=r"$> 2 \,\mathrm{p.e.}$")
ax2.plot(surv["eff"], surv["surviving_photons"], "x:", color="C3")

ax.legend()
# ax2.legend()

ax.set_ylabel("Selected Signal / True Photons", fontsize=10)
ax2.set_ylabel("Surviving Photons / True Photons", fontsize=10)

# ax.set_xlabel("Efficiency")
ax2.set_xlabel("Efficiency")

plt.savefig("build/surv.pdf", bbox_inches="tight")