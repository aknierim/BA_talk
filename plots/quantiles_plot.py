import numpy as np
import matplotlib.pyplot as plt

from ctapipe.io import TableLoader


QUANTILES = [0.995, 0.999, 0.9992, 0.9995, 0.9997, 0.9999]


input_file = "./plots/data/quantiles/gamma-diffuse_run_980_to_999_dark_cone10_merged.dl1.h5"
loader = TableLoader(input_file, load_dl1_images=True, load_dl2=False, load_instrument=False, load_simulated=False, load_true_images=True, load_true_parameters=False)

events = loader.read_telescope_events()

bins = np.logspace(-1.0, 4.0, 101)
hist_kwargs = dict(
    bins=bins,
    histtype='step',
    cumulative=-1,
)


fig, ax = plt.subplots(1, 1, figsize=(8, 3))

pixel_values = events['image'].ravel()
true_pixel_value = events['true_image'].ravel()
noise = pixel_values[true_pixel_value == 0]

ax.hist(pixel_values, label='All Pixels', **hist_kwargs)
ax.hist(noise, label='Noise Pixels', **hist_kwargs)
quantiles = np.quantile(noise, QUANTILES)

for v, q, alpha in zip(quantiles, QUANTILES, np.linspace(0.3, 1.0, len(QUANTILES))):
    plt.axvline(v, color='C2', alpha=alpha, label=f"Q({q:.2%}) = {v:.2f}", lw=1)

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_title(rf'Picture Quantiles for \texttt{{MST\_MST\_NectarCam}}')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Pixel Value / p.e.')
ax.set_ylabel('Pixel Counts')

plt.savefig(f"build/quantiles_plot.pdf", dpi=300, bbox_inches='tight')
