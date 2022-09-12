import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

plt.rc('axes', labelsize=16)

INPUT_BASE = "./plots/data/processed"


def plot_eff_area(
    ax: matplotlib.axes.Axes,
    tail,
    mars,
    fact,
    tcc,
    energy_unit: str="TeV"
) -> matplotlib.axes.Axes:


    eff_tail = tail["n_reco"].sum() / tail["n_total"].sum()
    eff_mars = mars["n_reco"].sum() / mars["n_total"].sum()
    eff_fact = fact["n_reco"].sum() / fact["n_total"].sum()
    eff_tcc = tcc["n_reco"].sum() / tcc["n_total"].sum()

    ax.errorbar(
        tail["true_energy_center"],
        tail["aeff"],
        xerr=0.5 * tail["bin_width"],
        linestyle="",
        label=rf"Tailcuts, $\mathrm{{Eff}}$ = {eff_tail:.3f}"
    )

    ax.errorbar(
        mars["true_energy_center"],
        mars["aeff"],
        xerr=0.5 * mars["bin_width"],
        linestyle="",
        label=rf"MARS, $\mathrm{{Eff}}$ = {eff_mars:.3f}"
    )

    ax.errorbar(
        fact["true_energy_center"],
        fact["aeff"],
        xerr=0.5 * fact["bin_width"],
        linestyle="",
        label=rf"FACT, $\mathrm{{Eff}}$ = {eff_fact:.3f}"
    )

    ax.errorbar(
        tcc["true_energy_center"],
        tcc["aeff"],
        xerr=0.5 * tcc["bin_width"],
        linestyle="",
        label=rf"TCC, $\mathrm{{Eff}}$ = {eff_tcc:.3f}"
    )

    # alternative label: $\sum n_{{\mathrm{{reco}}}} \,/\, \sum n_{{\mathrm{{total}}}}$

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(
        rf"$E_{{\mathrm{{true}}}} \,\, / \,\, \mathrm{{{energy_unit}}}$"
    )
    ax.set_ylabel(r"$n_\mathrm{reco} \;/\; n_\mathrm{total}$")

    ax.legend(fontsize=12)

    return ax


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
        label=rf"Tailcuts, $\mathrm{{Mean Ang.Res.}} = {np.mean(tail['angular_resolution']):.3f}$"
    )
    ax.errorbar(
        mars["true_energy_center"],
        mars["angular_resolution"],
        xerr=mars["bin_width"] / 2,
        ls="",
        label=rf"MARS, $\mathrm{{Mean Ang.Res.}} = {np.mean(mars['angular_resolution']):.3f}$"
    )
    ax.errorbar(
        fact["true_energy_center"],
        fact["angular_resolution"],
        xerr=fact["bin_width"] / 2,
        ls="",
        label=rf"FACT, $\mathrm{{Mean Ang.Res.}} = {np.mean(fact['angular_resolution']):.3f}$"
    )
    ax.errorbar(
        tcc["true_energy_center"],
        tcc["angular_resolution"],
        xerr=tcc["bin_width"] / 2,
        ls="",
        label=rf"TCC, $\mathrm{{Mean Ang.Res.}} = {np.mean(tcc['angular_resolution']):.3f}$"
    )

    ax.set_ylabel(r'Angular Resolution $\theta_{68\%} \,\, / \,\, \mathrm{deg}$')
    ax.set_xlabel(r'$E_{\mathrm{true}} \,\,/\,\, \mathrm{TeV}$')
    ax.set_xscale('log')

    ax.set_ylim(0, 1.4)

    ax.legend(fontsize=12)

    return ax

def plot_combined(
    ids: int,
    energy_unit: str="TeV"
):
    tail = pd.read_csv(f"{INPUT_BASE}/MST_MST_NectarCam/angular_resolution/tailcuts/ang_res_MST_MST_NectarCam_id_{ids[0]}.csv")
    mars = pd.read_csv(f"{INPUT_BASE}/MST_MST_NectarCam/angular_resolution/mars/ang_res_MST_MST_NectarCam_id_{ids[1]}.csv")
    fact = pd.read_csv(f"{INPUT_BASE}/MST_MST_NectarCam/angular_resolution/fact/ang_res_MST_MST_NectarCam_id_{ids[2]}.csv")
    tcc = pd.read_csv(f"{INPUT_BASE}/MST_MST_NectarCam/angular_resolution/tcc/ang_res_MST_MST_NectarCam_id_{ids[3]}.csv")

    size = plt.gcf().get_size_inches()
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(size[0], size[1]*2.5), constrained_layout=True, sharex=True, dpi=300)

    ax = plot_ang_res(ax, tail, mars, fact, tcc)
    ax2 = plot_eff_area(ax2, tail, mars, fact, tcc, energy_unit)

    return fig, ax, ax2


def main():
    df_angres = pd.read_csv('plots/data/combined_table.csv')

    for index in range(len(df_angres)):
        nlower = df_angres['n_lower'].loc[index]
        nupper = nlower + 0.05

        ids = df_angres.iloc[[index],1:5]

        if not ids.loc[index].isnull().any().any():

            ids = ids.astype(int)
            ids = ids.values.tolist()

            fig, ax, ax2 = plot_combined(ids[0])

            fig.suptitle(rf"${nlower:.2f} \leq \mathrm{{Efficiency}} < {nupper:.2f}$")

            plt.savefig(f'plots/ar_aeff/AR_Aeff_MST_{nlower:.2f}_{nupper:.2f}.pdf')
            plt.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e

    fig, ax, ax2 = plot_combined([101, 13, 974, 1954])
    ax2.set_ylim(1e-2, 1)
    fig.suptitle(r"$0.40 \leq \mathrm{Efficiency} < 0.45$")
    plt.savefig(f'plots/ar_aeff/AR_Aeff_MST_0.40_0.45.pdf')

    # fig, ax, ax2 = plot_combined([118, 54, 767, 367])
    # fig.suptitle(r"$0.10 \leq \mathrm{Efficiency} < 0.15$")
    # plt.savefig(f'plots/ar_aeff/AR_Aeff_MST_0.10_0.15.pdf')