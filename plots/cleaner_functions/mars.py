from .tail import tail_2
import numpy as np

def mars_1(
    geom,
    image,
    picture_thresh=5.5,
    boundary_thresh=1.833,
    keep_isolated_pixels=False,
    min_number_picture_neighbors=2,
):
    pixels_above_picture = image >= picture_thresh

    if keep_isolated_pixels or min_number_picture_neighbors == 0:
        pixels_in_picture = pixels_above_picture
    else:
        # Require at least min_number_picture_neighbors. Otherwise, the pixel
        #  is not selected
        number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
            pixels_above_picture.view(np.byte)
        )
        pixels_in_picture = pixels_above_picture & (
            number_of_neighbors_above_picture >= min_number_picture_neighbors
        )
    return pixels_in_picture

def mars_2(
    geom,
    image,
    picture_thresh=5.5,
    boundary_thresh=1.833,
    keep_isolated_pixels=False,
    min_number_picture_neighbors=2,
):
    pixels_above_picture = image >= picture_thresh

    if keep_isolated_pixels or min_number_picture_neighbors == 0:
        pixels_in_picture = pixels_above_picture
    else:
        # Require at least min_number_picture_neighbors. Otherwise, the pixel
        #  is not selected
        number_of_neighbors_above_picture = geom.neighbor_matrix_sparse.dot(
            pixels_above_picture.view(np.byte)
        )
        pixels_in_picture = pixels_above_picture & (
            number_of_neighbors_above_picture >= min_number_picture_neighbors
        )

    # by broadcasting together pixels_in_picture (1d) with the neighbor
    # matrix (2d), we find all pixels that are above the boundary threshold
    # AND have any neighbor that is in the picture
    pixels_above_boundary = image >= boundary_thresh
    pixels_with_picture_neighbors = geom.neighbor_matrix_sparse.dot(pixels_in_picture)
    if keep_isolated_pixels:
        return (
            pixels_above_boundary & pixels_with_picture_neighbors
        ) | pixels_in_picture
    else:
        pixels_with_boundary_neighbors = geom.neighbor_matrix_sparse.dot(
            pixels_above_boundary
        )
        return (pixels_above_boundary & pixels_with_picture_neighbors) | (
            pixels_in_picture & pixels_with_boundary_neighbors
        )

def mars_3(
    geom,
    image,
    picture_thresh=5.5,
    boundary_thresh=1.833,
    keep_isolated_pixels=False,
    min_number_picture_neighbors=2,
):
    pixels_from_tailcuts_clean = tail_2(
        geom,
        image,
        picture_thresh,
        boundary_thresh,
        keep_isolated_pixels,
        min_number_picture_neighbors,
    )
    pixels_above_2nd_boundary = image >= boundary_thresh

    # and now it's the same as the last part of 'tailcuts_clean', but without
    # the core pixels, i.e. we start from the neighbors of the core pixels.
    pixels_with_previous_neighbors = geom.neighbor_matrix_sparse.dot(
        pixels_from_tailcuts_clean
    )
    if keep_isolated_pixels:
        return (
            pixels_above_2nd_boundary & pixels_with_previous_neighbors
        ) | pixels_from_tailcuts_clean
    else:
        pixels_with_2ndboundary_neighbors = geom.neighbor_matrix_sparse.dot(
            pixels_above_2nd_boundary
        )
        return (pixels_above_2nd_boundary & pixels_with_previous_neighbors) | (
            pixels_from_tailcuts_clean & pixels_with_2ndboundary_neighbors
        )