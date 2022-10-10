from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

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


def color_shades(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def metrics_bar_plot(
        cleaner,
        size,
        color,
        width=0.15
    ):

    data = pd.read_csv(f'plots/data/metrics/metrics_{cleaner}_MST_MST_NectarCam.csv')
    efficiency = pd.read_csv('plots/data/combined_table.csv')

    if not cleaner == 'tailcuts':
        cln = cleaner
    else:
        cln = 'tail'

    eff_idx = efficiency[f'index_{cln}']
    eff_idx = eff_idx.dropna().astype(int)
    efficiency = efficiency[f'ratio_{cln}'].iloc[eff_idx.index]


    data = data.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn", "FPR", "PPV"])
    labels = [metrics_dict[k] for k in data.keys()]
    x_ticks = np.arange(len(labels))

    interval = np.linspace(-len(data)/2, len(data)/2, len(data))
    # print(interval)

    fig, ax = plt.subplots(1, 1, figsize=(size[0]*2, size[1]))
    for idx, alpha in zip(range(len(data)), np.linspace(0.2, 1.0, len(data))):
        ax.bar(x_ticks + interval[idx]*width, data.iloc[idx], width, color=color, alpha=alpha, label=f'{efficiency.iloc[idx]:.3f}')

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(data.keys())
    ax.set_ylim(0, 1.05)

    ax.axhline(1.0, ls="dotted", alpha=0.4, color="black")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Efficiency")

    # ax.set_title(rf'\gls{{mst}} Metrics', fontsize=12)

    plt.savefig(f"build/metrics_{cleaner}_{args.theme}.pdf", bbox_inches='tight', dpi=300)
    plt.close()


def metrics_bar_plot_all(
    row_idx,
    width=0.15
):

    tail = pd.read_csv('plots/data/metrics/metrics_tailcuts_MST_MST_NectarCam.csv')
    mars = pd.read_csv('plots/data/metrics/metrics_mars_MST_MST_NectarCam.csv')
    fact = pd.read_csv('plots/data/metrics/metrics_fact_MST_MST_NectarCam.csv')
    tcc = pd.read_csv('plots/data/metrics/metrics_tcc_MST_MST_NectarCam.csv')

    tail = tail.iloc[[row_idx],:]
    mars = mars.iloc[[row_idx],:]
    fact = fact.iloc[[row_idx],:]
    tcc = tcc.iloc[[row_idx],:]

    df = pd.concat([tail, mars, fact, tcc])
    # print(df)

    df = df.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn", "FPR", "PPV"])
    labels = [metrics_dict[k] for k in df.keys()]
    x_ticks = np.arange(len(labels))

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(df)]
    names = ["Tailcuts", "MARS", "FACT", "TCC"]

    interval = np.linspace(-len(df)/2, len(df)/2, len(df))

    fig, ax = plt.subplots(1, 1, figsize=(size[0]*2, size[1]))
    for idx, color, label in zip(range(len(df)), colors, names):
        ax.bar(x_ticks + interval[idx]*width, df.iloc[idx], width, color=color, label=label, alpha=0.7)

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(df.keys())
    ax.set_ylim(0, 1.05)

    ax.axhline(1.0, ls="dotted", alpha=0.4, color="black")
    ax.legend()

    # ax.set_title(rf'\gls{{mst}} Metrics', fontsize=12)

    plt.savefig(f"build/metrics_all_{args.theme}.pdf", bbox_inches='tight', dpi=300)
    plt.close()



if __name__ == "__main__":

    args = parser.parse_args()

    if args.theme == 'dark':
        plt.style.use('plots/darkmode.mplstyle')

    size = plt.gcf().get_size_inches()

    metrics_bar_plot("tailcuts", size=size, color='C0', width=0.1)
    metrics_bar_plot("mars", size=size, color='C1', width=0.1)
    metrics_bar_plot("fact", size=size, color='C2', width=0.09)
    metrics_bar_plot("tcc", size=size, color='C3', width=0.1)

    # with open('configs/tailcuts/tailcuts_clean_mst_6.200_4.650_mn_2_config.yml') as f:
    #     my_dict = yaml.safe_load(f)

    # settings = {
    #     'picture_thresh': my_dict['ImageProcessor']['TailcutsImageCleaner']['picture_threshold_pe'][0][2],
    #     'boundary_thresh': my_dict['ImageProcessor']['TailcutsImageCleaner']['boundary_threshold_pe'][0][2],
    #     'min_picture_neighbors': my_dict['ImageProcessor']['TailcutsImageCleaner']['min_picture_neighbors'],
    # }

    # print(settings.values())

    metrics_bar_plot_all(row_idx=-1)