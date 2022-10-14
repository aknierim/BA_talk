from argparse import ArgumentParser
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

from colour import Color

from ctapipe.visualization import CameraDisplay
from ctapipe.io import TableLoader

from ctapipe.visualization import CameraDisplay

from cleaner_functions.tail import tail_1, tail_2
from cleaner_functions.mars import mars_1, mars_2, mars_3
from cleaner_functions.fact import fact_1, fact_2, fact_3, fact_4, fact_5, fact_6
from cleaner_functions.tcc import tcc_1, tcc_2, tcc_3, tcc_4, tcc_5


parser = ArgumentParser()

parser.add_argument('--theme',
                    default='light',
                    nargs='?',
                    choices=['light', 'dark'],
                    help="""The theme for the plots. Choose from 'light' and 'dark'
                    \n(default: %(default)s)
                    """
)


# Custom cmap
def custom_cmap(color_list: list) -> LinearSegmentedColormap:
    """Creates a colormap to a given list of colors.
    Also provides a preview of the colormap via plt.imshow().

    Parameters:
    -----------
    ramp_colors: list
        List of hexadecimal color codes with leading number sign (#).

    Returns:
    --------
    cmap: LinearSegmentedColormap
        A colormap containing the given colors.
    """

    cmap = LinearSegmentedColormap.from_list(
        'my_list', [Color(c1).rgb for c1 in color_list]
    )
    plt.figure(figsize = (15,3))
    plt.imshow(
        [list(np.arange(0, len(color_list), 0.1))],
        interpolation='nearest',
        origin='lower',
        cmap=cmap
    )
    plt.xticks([])
    plt.yticks([])

    return cmap





def mask_image(current_mask, previous_mask):
    mask_img = np.array(current_mask).astype(int)

    mask_img[np.bitwise_xor(current_mask, previous_mask) & previous_mask] = 2
    mask_img[np.bitwise_xor(current_mask, previous_mask) & current_mask] = 3

    mask_img = np.array(mask_img, dtype=float)

    mask_img[mask_img == 1] = 7/10 # selected
    mask_img[mask_img == 2] = 3/10 # removed
    mask_img[mask_img == 3] = 10/10 # new

    #create patches
    cmap = masks_image_cmap
    color_tp = cmap(10/10) #TP
    color_fp = cmap(7/10) #FP
    color_fn = cmap(3/10) #FN
    color_tn = cmap(0)    #TN

    tp_patch = mpatches.Patch(color=color_tp, label=f'newly selected')
    fp_patch = mpatches.Patch(color=color_fp, label=f'already selected')
    fn_patch = mpatches.Patch(color=color_fn, label=f'removed')
    tn_patch = mpatches.Patch(color=color_tn, label=f'not selected')

    return mask_img, tp_patch, fp_patch, fn_patch, tn_patch


#   ============================================================================

# Tailcuts
def set_image_tail_1(cleaner, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    null_mask = np.zeros(len(mask), dtype=bool)

    disp = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning 1st Step")
    disp.cmap = masks_image_cmap


    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, null_mask)
    disp.image = mask_img
    disp.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch], loc=0)
    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


def set_image_tail_2(cleaner, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    null_mask = np.zeros(len(mask), dtype=bool)

    disp = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning 2nd Step")
    disp.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask2, mask)
    disp.image = mask_img
    disp.set_limits_minmax(0, 1)
    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])
    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]
    return handles


# MARS
def set_image_mars(cleaner, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning 3rd Step")
    disp2.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, mask2)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])

    axs.set_axis_off()

    handles = [tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


# FACT
def set_image_fact_1(cleaner, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    null_mask = np.zeros(len(mask), dtype=bool)

    disp2 = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning 1st Step")
    disp2.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, null_mask)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


def set_image_fact_2(cleaner, step, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning {step} Step")
    disp2.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, mask2)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


# TCC
def set_image_tcc_1(cleaner, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    null_mask = np.zeros(len(mask), dtype=bool)

    disp2 = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning 1st Step")
    disp2.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, null_mask)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


def set_image_tcc_2(cleaner, step, mask, mask2, legend, axs):

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, title=f"{cleaner} Cleaning {step} Step")
    disp2.cmap = masks_image_cmap

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = mask_image(mask, mask2)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch])

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles

# ==============================================================================

# Tailcuts
def tail_plot():

    mask_tail_1 = []
    mask_tail_2 = []
    for event, arrival_times in zip(image, peak_time):
        mask_tail_1.append(tail_1(geom, event))
        mask_tail_2.append(tail_2(geom, event))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11,5), constrained_layout=True)
    handles = set_image_tail_1('Tailcuts', mask_tail_1, mask_tail_2, legend=False, axs=ax1)
    set_image_tail_2('Tailcuts', mask_tail_1, mask_tail_2, legend=False, axs=ax2)

    legend = fig.legend(bbox_to_anchor=(0.05, -0.1, 0.9, -0.05), loc="lower left",
                    mode="expand", borderaxespad=0, ncol=4, handles=handles, fontsize=20)



    plt.savefig(f"build/tailcuts_{args.theme}.pdf", bbox_inches="tight")


# MARS
def mars_plot():

    mask_mars_1 = []
    mask_mars_2 = []
    mask_mars_3 = []
    for event, arrival_times in zip(image, peak_time):
        mask_mars_1.append(mars_1(geom, event))
        mask_mars_2.append(mars_2(geom, event))
        mask_mars_3.append(mars_3(geom, event))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 5), constrained_layout=True)
    set_image_tail_1('MARS', mask_mars_1, mask_mars_2, legend=False, axs=ax1)
    handles = set_image_tail_2('MARS', mask_mars_1, mask_mars_2, legend=False, axs=ax2)
    set_image_mars('MARS', mask_mars_3, mask_mars_2, legend=False, axs=ax3)

    legend = fig.legend(bbox_to_anchor=(0.2, -0.1, 0.6, -0.05), loc="lower center",
                    mode="expand", borderaxespad=0, ncol=4, handles=handles, fontsize=20)



    plt.savefig(f"build/mars_{args.theme}.pdf", bbox_inches="tight")


# FACT
def fact_plot():

    fc1 = []
    fc2 = []
    fc3 = []
    fc4 = []
    fc5 = []
    fc6 = []
    for event, arrival_times in zip(image, peak_time):
        fc1.append(fact_1(geom, event, arrival_times))
        fc2.append(fact_2(geom, event, arrival_times))
        fc3.append(fact_3(geom, event, arrival_times))
        fc4.append(fact_4(geom, event, arrival_times))
        fc5.append(fact_5(geom, event, arrival_times))
        fc6.append(fact_6(geom, event, arrival_times))

    fig, ax = plt.subplots(2, 3, figsize=(17, 10), constrained_layout=True)
    ax = ax.flatten()
    handles = set_image_fact_1('FACT', fc1, fc1, legend=False, axs=ax[0])
    set_image_fact_2('FACT', '2nd', fc2, fc1, legend=False, axs=ax[1])
    set_image_fact_2('FACT', '3rd', fc3, fc2, legend=False, axs=ax[2])
    set_image_fact_2('FACT', '4th', fc4, fc3, legend=False, axs=ax[3])
    set_image_fact_2('FACT', '5th', fc5, fc4, legend=False, axs=ax[4])
    set_image_fact_2('FACT', '6th', fc6, fc5, legend=False, axs=ax[5])

    legend = fig.legend(bbox_to_anchor=(0.2, -0.05, 0.6, 0), loc="lower center",
                    mode="expand", borderaxespad=0, ncol=4, handles=handles, fontsize=20)



    plt.savefig(f"build/fact_{args.theme}.pdf", bbox_inches="tight")


# TCC
def tcc_plot():

    tcc1 = []
    tcc2 = []
    tcc3 = []
    tcc4 = []
    tcc5 = []
    for event, arrival_times in zip(image, peak_time):
        tcc1.append(tcc_1(geom, event, arrival_times))
        tcc2.append(tcc_2(geom, event, arrival_times))
        tcc3.append(tcc_3(geom, event, arrival_times))
        tcc4.append(tcc_4(geom, event, arrival_times))
        tcc5.append(tcc_5(geom, event, arrival_times))

    fig = plt.figure(figsize=(17, 10))
    gs = gridspec.GridSpec(2, 6)

    axs = []

    for i in range(0, 5):
        if i < 3:
            ax = plt.subplot(gs[0, 2 * i:2 * i + 2])
        else:
            ax = plt.subplot(gs[1, 2 * i - 5:2 * i + 2 - 5])

        axs.append(ax)

    handles = set_image_tcc_1('TCC', tcc1, tcc1, legend=False, axs=axs[0])
    set_image_tcc_2('TCC', '2nd', tcc2, tcc1, legend=False, axs=axs[1])
    set_image_tcc_2('TCC', '3rd', tcc3, tcc2, legend=False, axs=axs[2])
    set_image_tcc_2('TCC', '4th', tcc4, tcc3, legend=False, axs=axs[3])
    set_image_tcc_2('TCC', '5th', tcc5, tcc4, legend=False, axs=axs[4])

    legend = fig.legend(bbox_to_anchor=(0.2, 0.07, 0.6, 0.12), loc="lower center",
                    mode="expand", borderaxespad=0, ncol=4, handles=handles, fontsize=20)

    plt.savefig(f"build/tcc_{args.theme}.pdf", bbox_inches='tight')


if __name__ == "__main__":
    args = parser.parse_args()

    if args.theme == "dark":
        plt.style.use('darkmode.mplstyle')

    masks_image_cmap = custom_cmap(['#2e2e2e', '#b00e0e', '#ffffff', '#ffffff', '#44c949'])

    loader = TableLoader(
        'plots/data/steps_improved/gamma-diffuse_run_990_to_999_dark_cone10_merged.dl1.h5',
        load_dl1_images=True,
        load_dl1_parameters=True,
        load_dl2=True,
        load_instrument=True,
        load_simulated=True,
        load_true_images=True,
        load_true_parameters=True,

    )


    data = loader.read_telescope_events_by_type()
    subarray = loader.subarray

    tel_type = ["MST_MST_NectarCam", 5]
    geom = subarray.tel[tel_type[1]].camera.geometry

    image = data[tel_type[0]]['image'][214]
    peak_time = data[tel_type[0]]['peak_time'][214]
    # print(data)

    # tail_plot()
    # mars_plot()
    fact_plot()
    tcc_plot()