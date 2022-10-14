import numpy as np

def fact_1(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold
    return pixels_to_keep

def fact_2(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold

    # Step 2
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (
        number_of_neighbors_above_picture >= min_number_neighbors
    )
    return pixels_to_keep

def fact_3(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold

    # Step 2
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (
        number_of_neighbors_above_picture >= min_number_neighbors
    )

    # Step 3
    pixels_above_boundary = image >= boundary_threshold
    pixels_to_keep = dilate(geom, pixels_to_keep) & pixels_above_boundary

    # nothing else to do if min_number_neighbors <= 0
    if min_number_neighbors <= 0:
        return pixels_to_keep

    return pixels_to_keep


def fact_4(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold

    # Step 2
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (
        number_of_neighbors_above_picture >= min_number_neighbors
    )

    # Step 3
    pixels_above_boundary = image >= boundary_threshold
    pixels_to_keep = dilate(geom, pixels_to_keep) & pixels_above_boundary

    # nothing else to do if min_number_neighbors <= 0
    if min_number_neighbors <= 0:
        return pixels_to_keep

    # Step 4
    pixels_to_keep = apply_time_delta_cleaning(
        geom, pixels_to_keep, arrival_times, min_number_neighbors, time_limit
    )
    return pixels_to_keep


def fact_5(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold

    # Step 2
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (
        number_of_neighbors_above_picture >= min_number_neighbors
    )

    # Step 3
    pixels_above_boundary = image >= boundary_threshold
    pixels_to_keep = dilate(geom, pixels_to_keep) & pixels_above_boundary

    # nothing else to do if min_number_neighbors <= 0
    if min_number_neighbors <= 0:
        return pixels_to_keep

    # Step 4
    pixels_to_keep = apply_time_delta_cleaning(
        geom, pixels_to_keep, arrival_times, min_number_neighbors, time_limit
    )

    # Step 5
    number_of_neighbors = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (number_of_neighbors >= min_number_neighbors)
    return pixels_to_keep

def fact_6(
    geom,
    image,
    arrival_times,
    picture_threshold=4.2,
    boundary_threshold=1.4,
    min_number_neighbors=2,
    time_limit=6.0,
):
    # Step 1
    pixels_to_keep = image >= picture_threshold

    # Step 2
    number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (
        number_of_neighbors_above_picture >= min_number_neighbors
    )

    # Step 3
    pixels_above_boundary = image >= boundary_threshold
    pixels_to_keep = dilate(geom, pixels_to_keep) & pixels_above_boundary

    # nothing else to do if min_number_neighbors <= 0
    if min_number_neighbors <= 0:
        return pixels_to_keep

    # Step 4
    pixels_to_keep = apply_time_delta_cleaning(
        geom, pixels_to_keep, arrival_times, min_number_neighbors, time_limit
    )

    # Step 5
    number_of_neighbors = geom.neighbor_matrix_sparse.dot(
        (pixels_to_keep).view(np.byte)
    )
    pixels_to_keep = pixels_to_keep & (number_of_neighbors >= min_number_neighbors)

    # Step 6
    pixels_to_keep = apply_time_delta_cleaning(
        geom, pixels_to_keep, arrival_times, min_number_neighbors, time_limit
    )
    return pixels_to_keep

def dilate(geom, mask):
    """
    Add one row of neighbors to the True values of a pixel mask and return
    the new mask.
    This can be used to include extra rows of pixels in a mask that was
    pre-computed, e.g. via `tailcuts_clean`.
    Parameters
    ----------
    geom: `~ctapipe.instrument.CameraGeometry`
        Camera geometry information
    mask: ndarray
        input mask (array of booleans) to be dilated
    """
    return mask | geom.neighbor_matrix_sparse.dot(mask)

def apply_time_delta_cleaning(
    geom, mask, arrival_times, min_number_neighbors, time_limit
):
    """
    Identify all pixels from selection that have less than N
    neighbors that arrived within a given timeframe.
    Parameters
    ----------
    geom: `ctapipe.instrument.CameraGeometry`
        Camera geometry information
    mask: array, boolean
        boolean mask of *clean* pixels before time_delta_cleaning
    arrival_times: array
        pixel timing information
    min_number_neighbors: int
        Threshold to determine if a pixel survives cleaning steps.
        These steps include checks of neighbor arrival time and value
    time_limit: int or float
        arrival time limit for neighboring pixels
    Returns
    -------
    A boolean mask of *clean* pixels.
    """
    pixels_to_keep = mask.copy()
    time_diffs = np.abs(arrival_times[mask, None] - arrival_times)
    # neighboring pixels arriving in the time limit and previously selected
    valid_neighbors = (time_diffs < time_limit) & geom.neighbor_matrix[mask] & mask
    enough_neighbors = np.count_nonzero(valid_neighbors, axis=1) >= min_number_neighbors
    pixels_to_keep[pixels_to_keep] &= enough_neighbors
    return pixels_to_keep