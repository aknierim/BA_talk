from argparse import ArgumentParser
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from ctapipe.io import TableLoader
from ctapipe.visualization import CameraDisplay

from cleaner_functions.tail import tail_2
from cleaner_functions.mars import mars_3
from cleaner_functions.fact import fact_6
from cleaner_functions.tcc import tcc_5


parser = ArgumentParser()

parser.add_argument('--theme',
                    default='light',
                    nargs='?',
                    choices=['light', 'dark'],
                    help="""The theme for the plots. Choose from 'light' and 'dark'
                    \n(default: %(default)s)
                    """
)


SIZE = plt.gcf().get_size_inches()


def classification_img(image_mask, true_image):

    class_img = (image_mask + (2*(true_image>0))).astype('float')

    # change values between 0..1 for colormapping
    class_img[class_img == 1] = 6/10 #FP
    class_img[class_img == 2] = 3/10 #FN
    class_img[class_img == 3] = 9/10 #TP

    cmap = plt.cm.get_cmap('gnuplot2')
    color_tp = cmap(9/10) #TP
    color_fp = cmap(6/10) #FP
    color_fn = cmap(3/10) #FN
    color_tn = cmap(0)    #TN

    tp_patch = mpatches.Patch(color=color_tp, label=f'TP ({len(class_img[class_img == 9/10])})')
    fp_patch = mpatches.Patch(color=color_fp, label=f'FP ({len(class_img[class_img == 6/10])})')
    fn_patch = mpatches.Patch(color=color_fn, label=f'FN ({len(class_img[class_img == 3/10])})')
    tn_patch = mpatches.Patch(color=color_tn, label=f'TN ({len(class_img[class_img == 0])})')

    return class_img, tp_patch, fp_patch, fn_patch, tn_patch


# Tailcuts
def set_image_tail_2(index, title, mask, true_image, legend, axs):

    mask = mask[index]
    true_image = true_image[index]

    axs.set_facecolor('0.1')

    disp = CameraDisplay(geom, ax=axs, show_frame=False, title=title)
    disp.cmap = plt.cm.gnuplot2

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = classification_img(mask, true_image)
    disp.image = mask_img
    disp.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch], loc=3)
    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]
    return handles


# MARS
def set_image_mars(index, title, mask, true_image, legend, axs):

    mask = mask[index]
    true_image = true_image[index]

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, show_frame=False, title=title)
    disp2.cmap = plt.cm.gnuplot2

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = classification_img(mask, true_image)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch], loc=3)

    axs.set_axis_off()

    handles = [tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


# FACT
def set_image_fact_2(index, title, mask, true_image, legend, axs):

    mask = mask[index]
    true_image = true_image[index]

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, show_frame=False, title=title)
    disp2.cmap = plt.cm.gnuplot2

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = classification_img(mask, true_image)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch], loc=3)

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles


# TCC
def set_image_tcc_2(index, title, mask, true_image, legend, axs):

    mask = mask[index]
    true_image = true_image[index]

    axs.set_facecolor('0.1')

    disp2 = CameraDisplay(geom, ax=axs, show_frame=False, title=title)
    disp2.cmap = plt.cm.gnuplot2

    mask_img, tp_patch, fp_patch, fn_patch, tn_patch = classification_img(mask, true_image)
    disp2.image = mask_img
    disp2.set_limits_minmax(0, 1)

    if legend == True:
        axs.legend(handles=[tp_patch, fp_patch, fn_patch, tn_patch], loc=3)

    axs.set_axis_off()

    handles=[tp_patch, fp_patch, fn_patch, tn_patch]

    return handles



def tailcuts_class(index):
    mask_default = []
    mask = []
    for event in events_by_type[tel_type[0]]['image']:
        mask_default.append(tail_2(geom, event, picture_thresh=7, boundary_thresh=5, min_number_picture_neighbors=0))
        mask.append(tail_2(geom, event))

    fig, ax = plt.subplots(1, 2, figsize=(11,5), constrained_layout=True)
    ax = ax.flatten()

    set_image_tail_2(index, 'Default', mask_default, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[0])
    set_image_tail_2(index, 'Optimized', mask, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[1])

    # legend = fig.legend(bbox_to_anchor=(-0.2, -0.2, 1.4, 0), loc="lower left",
    #                 mode="expand", borderaxespad=0, ncol=4, handles=handles)

    plt.savefig(f"build/classifier_img/tail_class_{args.theme}.pdf", bbox_inches='tight')


def mars_class(index):
    mask_default = []
    mask = []
    for event in events_by_type[tel_type[0]]['image']:
        mask_default.append(mars_3(geom, event, picture_thresh=7, boundary_thresh=5, min_number_picture_neighbors=0))
        mask.append(mars_3(geom, event))

    fig, ax = plt.subplots(1, 2, figsize=(11,5), constrained_layout=True)
    ax = ax.flatten()

    set_image_mars(index, 'Default', mask_default, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[0])
    set_image_mars(index, 'Optimized', mask, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[1])

    # legend = fig.legend(bbox_to_anchor=(-0.2, -0.2, 1.4, 0), loc="lower left",
    #                 mode="expand", borderaxespad=0, ncol=4, handles=handles)

    plt.savefig(f"build/classifier_img/mars_class_{args.theme}.pdf", bbox_inches='tight')


def fact_class(index):
    mask_default = []
    mask = []
    for event, arrival_times in zip(events_by_type[tel_type[0]]['image'], events_by_type[tel_type[0]]['peak_time']):
        mask_default.append(fact_6(geom, event, arrival_times, picture_threshold=7, boundary_threshold=5, min_number_neighbors=2, time_limit=5.0))
        mask.append(fact_6(geom, event, arrival_times))

    fig, ax = plt.subplots(1, 2, figsize=(11,5), constrained_layout=True)
    ax = ax.flatten()

    set_image_fact_2(index, 'Default', mask_default, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[0])
    set_image_fact_2(index, 'Optimized', mask, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[1])

    # legend = fig.legend(bbox_to_anchor=(-0.2, -0.2, 1.4, 0), loc="lower left",
    #                 mode="expand", borderaxespad=0, ncol=4, handles=handles)

    plt.savefig(f"build/classifier_img/fact_class_{args.theme}.pdf", bbox_inches='tight')


def tcc_class(index):
    mask_default = []
    mask = []
    for event, arrival_times in zip(events_by_type[tel_type[0]]['image'], events_by_type[tel_type[0]]['peak_time']):
        mask_default.append(tcc_5(geom, event, arrival_times, picture_thresh=7, boundary_thresh=5, time_limit_core=4.5, time_limit_boundary=1.5, min_number_picture_neighbors=1))
        mask.append(tcc_5(geom, event, arrival_times))

    fig, ax = plt.subplots(1, 2, figsize=(11,5), constrained_layout=True)
    ax = ax.flatten()

    set_image_tcc_2(index, 'Default', mask_default, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[0])
    set_image_tcc_2(index, 'Optimized', mask, events_by_type[tel_type[0]]['true_image'], legend=True, axs=ax[1])

    # legend = fig.legend(bbox_to_anchor=(-0.2, -0.2, 1.4, 0), loc="lower left",
    #                 mode="expand", borderaxespad=0, ncol=4, handles=handles)

    plt.savefig(f"build/classifier_img/tcc_class_{args.theme}.pdf", bbox_inches='tight')



if __name__ == '__main__':
    args = parser.parse_args()

    if args.theme == "dark":
        plt.style.use('plots/darkmode.mplstyle')

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

    events_by_type = loader.read_telescope_events_by_type()
    subarray = loader.subarray

    tel_type = ["MST_MST_NectarCam", 5]
    geom = subarray.tel[tel_type[1]].camera.geometry


    tailcuts_class(214)
    mars_class(214)
    fact_class(214)
    tcc_class(214)



