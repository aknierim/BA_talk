import numpy as np
from ctapipe.image.morphology import number_of_islands, brightest_island

def tcc_1(
    geom,
    image,
    arrival_times,
    picture_thresh=6.7,
    boundary_thresh=1.675,
    time_limit_core=15.0,
    time_limit_boundary=9.0,
    min_number_picture_neighbors=1,
):
    # find core pixels that pass a picture threshold
    pixels_above_picture = image >= picture_thresh
    return pixels_above_picture


def tcc_2(
    geom,
    image,
    arrival_times,
    picture_thresh=6.7,
    boundary_thresh=1.675,
    time_limit_core=15.0,
    time_limit_boundary=9.0,
    min_number_picture_neighbors=1,
):
    # find core pixels that pass a picture threshold
    pixels_above_picture = image >= picture_thresh

    # require at least min_number_picture_neighbors
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        pixels_above_picture.view(np.byte)
    )
    pixels_in_picture = pixels_above_picture & (
        number_of_neighbors_above_picture >= min_number_picture_neighbors
    )
    return pixels_in_picture


def tcc_3(
    geom,
    image,
    arrival_times,
    picture_thresh=6.7,
    boundary_thresh=1.675,
    time_limit_core=15.0,
    time_limit_boundary=9.0,
    min_number_picture_neighbors=1,
):
    # find core pixels that pass a picture threshold
    pixels_above_picture = image >= picture_thresh

    # require at least min_number_picture_neighbors
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        pixels_above_picture.view(np.byte)
    )
    pixels_in_picture = pixels_above_picture & (
        number_of_neighbors_above_picture >= min_number_picture_neighbors
    )

    # keep core pixels whose arrival times are within a certain time limit of the average
    mask_core = apply_time_average_cleaning(
        geom, pixels_in_picture, image, arrival_times, picture_thresh, time_limit_core
    )

    return mask_core


def tcc_4(
    geom,
    image,
    arrival_times,
    picture_thresh=6.7,
    boundary_thresh=1.675,
    time_limit_core=15.0,
    time_limit_boundary=9.0,
    min_number_picture_neighbors=1,
):
    # find core pixels that pass a picture threshold
    pixels_above_picture = image >= picture_thresh

    # require at least min_number_picture_neighbors
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        pixels_above_picture.view(np.byte)
    )
    pixels_in_picture = pixels_above_picture & (
        number_of_neighbors_above_picture >= min_number_picture_neighbors
    )

    # keep core pixels whose arrival times are within a certain time limit of the average
    mask_core = apply_time_average_cleaning(
        geom, pixels_in_picture, image, arrival_times, picture_thresh, time_limit_core
    )

    # find boundary pixels that pass a boundary threshold
    pixels_above_boundary = image >= boundary_thresh
    pixels_with_picture_neighbors = geom.neighbor_matrix_sparse.dot(mask_core)
    mask_boundary = (pixels_above_boundary & pixels_with_picture_neighbors) & np.invert(
        mask_core
    )
    return (pixels_above_boundary & pixels_with_picture_neighbors)


def tcc_5(
    geom,
    image,
    arrival_times,
    picture_thresh=6.7,
    boundary_thresh=1.675,
    time_limit_core=15.0,
    time_limit_boundary=9.0,
    min_number_picture_neighbors=1,
):
    # find core pixels that pass a picture threshold
    pixels_above_picture = image >= picture_thresh

    # require at least min_number_picture_neighbors
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        pixels_above_picture.view(np.byte)
    )
    pixels_in_picture = pixels_above_picture & (
        number_of_neighbors_above_picture >= min_number_picture_neighbors
    )

    # keep core pixels whose arrival times are within a certain time limit of the average
    mask_core = apply_time_average_cleaning(
        geom, pixels_in_picture, image, arrival_times, picture_thresh, time_limit_core
    )

    # find boundary pixels that pass a boundary threshold
    pixels_above_boundary = image >= boundary_thresh
    pixels_with_picture_neighbors = geom.neighbor_matrix_sparse.dot(mask_core)
    mask_boundary = (pixels_above_boundary & pixels_with_picture_neighbors) & np.invert(
        mask_core
    )

    # keep boundary pixels whose arrival times are within a certain time limit of the neighboring core pixels
    mask_boundary = mask_boundary.copy()

    time_diffs = np.abs(arrival_times[mask_boundary, None] - arrival_times)
    valid_neighbors = (
        (time_diffs < time_limit_boundary)
        & geom.neighbor_matrix[mask_boundary]
        & mask_core
    )
    enough_neighbors = (
        np.count_nonzero(valid_neighbors, axis=1) >= min_number_picture_neighbors
    )
    mask_boundary[mask_boundary] &= enough_neighbors

    return mask_core | mask_boundary

def apply_time_average_cleaning(
    geom, mask, image, arrival_times, picture_thresh, time_limit
):
    """
    Extract all pixels that arrived within a given timeframe
    with respect to the time average of the pixels on the main island.
    In order to avoid removing signal pixels of large impact-parameter events,
    the time limit for bright pixels is doubled.
    Parameters
    ----------
    geom: `ctapipe.instrument.CameraGeometry`
        Camera geometry information
    mask: array, boolean
        boolean mask of *clean* pixels before time_delta_cleaning
    image: array
        pixel values
    arrival_times: array
        pixel timing information
    picture_thresh: float
        threshold above which time limit is extended twice its value
    time_limit: int or float
        arrival time limit w.r.t. the average time of the core pixels
    Returns
    -------
    A boolean mask of *clean* pixels.
    """
    mask = mask.copy()
    if np.count_nonzero(mask) > 0:

        # use main island (maximum charge) for time average calculation
        num_islands, island_labels = number_of_islands(geom, mask)
        mask_main = brightest_island(num_islands, island_labels, image)
        time_ave = np.average(arrival_times[mask_main], weights=image[mask_main] ** 2)

        time_diffs = np.abs(arrival_times[mask] - time_ave)
        time_limit_pixwise = np.where(
            image < (2 * picture_thresh), time_limit, time_limit * 2
        )[mask]

        mask[mask] &= time_diffs < time_limit_pixwise

    return mask