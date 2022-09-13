from argparse import ArgumentParser
import numpy as np
import pandas as pd
import matplotlib
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


metrics_dict = {
        "TPR": "True Positive Rate",
        "FPR": "False Positve Rate",
        "TNR": "True Negative Rate",
        "FNR": "False Negative Rate",
        "PPV": "Positive Predictive Value",
        "ACC": "Accuracy",
        "BA": "Balanced Accuracy"
    }


def metrics_bar_plot_all(
    row_idx,
    width=0.15
):

    tail = pd.read_csv('plots/data/metrics/metrics_tailcuts_MST_MST_NectarCam.csv')
    mars = pd.read_csv('plots/data/metrics/metrics_mars_MST_MST_NectarCam.csv')
    fact = pd.read_csv('plots/data/metrics/metrics_fact_MST_MST_NectarCam.csv')
    tcc = pd.read_csv('plots/data/metrics/metrics_tcc_MST_MST_NectarCam.csv')

    tail_b = pd.read_csv('plots/data/baseline/metrics_tailcuts_base.csv')
    mars_b = pd.read_csv('plots/data/baseline/metrics_mars_base.csv')
    fact_b = pd.read_csv('plots/data/baseline/metrics_fact_base.csv')
    tcc_b = pd.read_csv('plots/data/baseline/metrics_tcc_base.csv')

    tail = tail.iloc[[row_idx],:]
    mars = mars.iloc[[row_idx],:]
    fact = fact.iloc[[row_idx],:]
    tcc = tcc.iloc[[row_idx],:]

    df = pd.concat([tail, mars, fact, tcc])
    base = pd.concat([tail_b, mars_b, fact_b, tcc_b])

    df = df.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn", "FPR", "PPV"])
    base = base.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn", "FPR", "PPV"])

    labels = [metrics_dict[k] for k in df.keys()]
    x_ticks = np.arange(len(labels))

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(df)]
    names = ["Tailcuts", "MARS", "FACT", "TCC"]

    interval = np.linspace(-len(df)/2, len(df)/2, len(df))

    fig, ax = plt.subplots(1, 1, figsize=(size[0]*2, size[1]))
    for idx, color, label in zip(range(len(df)), colors, names):
        ax.bar(x_ticks + interval[idx]*width, df.iloc[idx], width, edgecolor=color, fill=False, label=label + ", this work", ls='-', lw=1.5)
        ax.bar(x_ticks + interval[idx]*width, base.iloc[idx], width, color=color, alpha=0.5, label=label + ", baseline")


    ax.set_xticks(x_ticks)
    ax.set_xticklabels(df.keys())
    ax.set_ylim(0, 1.05)

    ax.axhline(1.0, ls="dotted", alpha=0.4, color="black")
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # ax.set_title(rf'\gls{{mst}} Metrics', fontsize=12)

    plt.savefig(f"build/metrics_baseline.pdf", bbox_inches='tight', dpi=300)
    plt.close()


def plot_eff_area(
    ax: matplotlib.axes.Axes,
    tail,
    mars,
    fact,
    tcc,
    energy_unit: str="TeV"
) -> matplotlib.axes.Axes:


    mean_tail = tail["aeff"].mean()
    mean_mars = mars["aeff"].mean()
    mean_fact = fact["aeff"].mean()
    mean_tcc = tcc["aeff"].mean()

    ax.errorbar(
        tail["true_energy_center"],
        tail["aeff"],
        xerr=0.5 * tail["bin_width"],
        linestyle="",
        label=f"Tailcuts, Mean Efficiency = {mean_tail:.3f}"
    )

    ax.errorbar(
        mars["true_energy_center"],
        mars["aeff"],
        xerr=0.5 * mars["bin_width"],
        linestyle="",
        label=f"MARS, Mean Efficiency = {mean_mars:.3f}"
    )

    ax.errorbar(
        fact["true_energy_center"],
        fact["aeff"],
        xerr=0.5 * fact["bin_width"],
        linestyle="",
        label=f"FACT, Mean Efficiency = {mean_fact:.3f}"
    )

    ax.errorbar(
        tcc["true_energy_center"],
        tcc["aeff"],
        xerr=0.5 * tcc["bin_width"],
        linestyle="",
        label=f"TCC, Mean Efficiency = {mean_tcc:.3f}"
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(
        rf"$E_{{\mathrm{{true}}}} \,\, / \,\, \mathrm{{{energy_unit}}}$"
    )
    ax.set_ylabel(r"Efficiency $n_\mathrm{reco} \;/\; n_\mathrm{total}$")

    ax.legend(fontsize=12)


def plot_ang_res(
    ax: matplotlib.axes.Axes,
    tail,
    mars,
    fact,
    tcc
) -> matplotlib.axes.Axes:

    ax.errorbar(
        tail["true_energy_center"],
        tail["angular_resolution"],
        xerr=tail["bin_width"] / 2,
        ls="",
        label=rf"Tailcuts"
    )
    ax.errorbar(
        mars["true_energy_center"],
        mars["angular_resolution"],
        xerr=mars["bin_width"] / 2,
        ls="",
        label=rf"MARS"
    )
    ax.errorbar(
        fact["true_energy_center"],
        fact["angular_resolution"],
        xerr=fact["bin_width"] / 2,
        ls="",
        label=rf"FACT"
    )
    ax.errorbar(
        tcc["true_energy_center"],
        tcc["angular_resolution"],
        xerr=tcc["bin_width"] / 2,
        ls="",
        label=rf"TCC"
    )

    ax.set_ylabel(r'Rel. Angular Resolution $ \theta_{\SI{68}{\percent},\,\mathrm{rel}}$')
    ax.set_xlabel(r'$E_{\mathrm{true}} \,\,/\,\, \mathrm{TeV}$')
    ax.set_xscale('log')

    ax.set_ylim(0, 3.5)

    ax.legend(fontsize=12)

    return ax

def plot_combined(
    ids: int,
    energy_unit: str="TeV"
):
    tail = pd.read_csv(f"plots/data/processed/MST_MST_NectarCam/angular_resolution/tailcuts/ang_res_MST_MST_NectarCam_id_{ids[0]}.csv")
    mars = pd.read_csv(f"plots/data/processed/MST_MST_NectarCam/angular_resolution/mars/ang_res_MST_MST_NectarCam_id_{ids[1]}.csv")
    fact = pd.read_csv(f"plots/data/processed/MST_MST_NectarCam/angular_resolution/fact/ang_res_MST_MST_NectarCam_id_{ids[2]}.csv")
    tcc = pd.read_csv(f"plots/data/processed/MST_MST_NectarCam/angular_resolution/tcc/ang_res_MST_MST_NectarCam_id_{ids[3]}.csv")

    tail_b = pd.read_csv("plots/data/baseline/angres_tailcuts_base.csv")
    mars_b = pd.read_csv("plots/data/baseline/angres_mars_base.csv")
    fact_b = pd.read_csv("plots/data/baseline/angres_fact_base.csv")
    tcc_b = pd.read_csv("plots/data/baseline/angres_tcc_base.csv")

    tail[["aeff", "angular_resolution"]] = tail[["aeff", "angular_resolution"]] / tail_b[["aeff", "angular_resolution"]]
    mars[["aeff", "angular_resolution"]] = mars[["aeff", "angular_resolution"]] / mars_b[["aeff", "angular_resolution"]]
    fact[["aeff", "angular_resolution"]] = fact[["aeff", "angular_resolution"]] / fact_b[["aeff", "angular_resolution"]]
    tcc[["aeff", "angular_resolution"]] = tcc[["aeff", "angular_resolution"]] / tcc_b[["aeff", "angular_resolution"]]

    size = plt.gcf().get_size_inches()
    fig, ax = plt.subplots(1, 1, figsize=(size[0], size[1]*1.25), constrained_layout=True, dpi=300)

    ax = plot_ang_res(ax, tail, mars, fact, tcc)

    return fig, ax


def ar_eff():
    df_angres = pd.read_csv('plots/data/combined_table.csv')

    for index in range(len(df_angres)):
        nlower = df_angres['n_lower'].loc[index]
        nupper = nlower + 0.05

        ids = df_angres.iloc[[index],1:5]

        if not ids.loc[index].isnull().any().any():

            ids = ids.astype(int)
            ids = ids.values.tolist()

            fig, ax = plot_combined(ids[0])

            # fig.suptitle(rf"${nlower:.2f} \leq \mathrm{{Efficiency}} < {nupper:.2f}$")

            plt.savefig(f'plots/ar_aeff/Rel_AR_{nlower:.2f}_{nupper:.2f}_base.pdf')
            plt.close()


if __name__ == "__main__":

    args = parser.parse_args()

    if args.theme == 'dark':
        plt.style.use('plots/darkmode.mplstyle')

    size = plt.gcf().get_size_inches()

    metrics_bar_plot_all(row_idx=-1)


    plt.rc('axes', labelsize=16)
    ar_eff()
