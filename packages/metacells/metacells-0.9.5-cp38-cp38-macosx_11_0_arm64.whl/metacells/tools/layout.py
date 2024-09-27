"""
Layout
------
"""

import warnings
from typing import Optional
from typing import Union

import numpy as np
import scipy.sparse as sp  # type: ignore
import umap  # type: ignore
from anndata import AnnData  # type: ignore

import metacells.parameters as pr
import metacells.utilities as ut

__all__ = [
    "umap_by_distances",
    "spread_coordinates",
]


@ut.logged()
@ut.timed_call()
@ut.expand_doc()
def umap_by_distances(
    adata: AnnData,
    distances: Union[str, ut.ProperMatrix] = "umap_distances",
    *,
    prefix: str = "",
    k: int = pr.umap_k,
    dimensions: int = 2,
    min_dist: float = pr.umap_min_dist,
    spread: float = pr.umap_spread,
    random_seed: int,
) -> None:
    """
    Compute layout for the observations using UMAP, based on a distances matrix.

    **Input**

    The input annotated ``adata`` is expected to contain a per-observation-per-observation property
    ``distances`` (default: {distances}), which describes the distance between each two observations
    (cells). The distances must be non-negative, symmetrical, and zero for self-distances (on the
    diagonal).

    **Returns**

    Sets the following annotations in ``adata``:

    Observation (Cell) Annotations
        ``<prefix>x``, ``<prefix>y``
            Coordinates for UMAP 2D projection of the observations (if ``dimensions`` is 2).
        ``<prefix>u``, ``<prefix>v``, ``<prefix>w``
            Coordinates for UMAP 3D projection of the observations (if ``dimensions`` is 3).

    **Computation Parameters**

    1. Invoke UMAP to compute a layout of some ``dimensions`` (default: {dimensions}D) using
       ``min_dist`` (default: {min_dist}), ``spread`` (default: {spread}) and ``k`` (default: {k}).
       If the spread is lower than the minimal distance, it is raised. If ``random_seed``
       is not zero, then it is passed to UMAP to force the computation to be
       reproducible. However, this means UMAP will use a single-threaded implementation that will be
       slower.
    """
    assert dimensions in (2, 3)
    if isinstance(distances, str):
        distances_matrix = ut.get_oo_proper(adata, distances)
    else:
        distances_matrix = distances
    # UMAP dies when given a dense matrix.
    distances_csr = sp.csr_matrix(distances_matrix)

    spread = max(min_dist, spread)  # UMAP insists.

    # UMAP implementation doesn't know to reduce K by itself.
    n_neighbors = min(k, adata.n_obs - 2)

    random_state: Optional[int] = None
    if random_seed != 0:
        random_state = random_seed

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            coordinates = umap.UMAP(
                metric="precomputed",
                n_neighbors=n_neighbors,
                spread=spread,
                min_dist=min_dist,
                n_components=dimensions,
                random_state=random_state,
            ).fit_transform(distances_csr)
    except ValueError:
        # UMAP implementation doesn't know how to handle too few edges.
        # However, it considers structural zeros as real edges.
        distances_matrix = ut.to_numpy_matrix(distances_matrix, copy=True)
        distances_matrix += 1.0
        np.fill_diagonal(distances_matrix, 0.0)
        distances_csr = sp.csr_matrix(distances_matrix)
        distances_csr.data -= 1.0
        coordinates = umap.UMAP(
            metric="precomputed", n_neighbors=n_neighbors, spread=spread, min_dist=min_dist, random_state=random_state
        ).fit_transform(distances_csr)

    all_sizes = []
    all_coordinates = []
    for axis in range(dimensions):
        axis_coordinates = ut.to_numpy_vector(coordinates[:, axis], copy=True)
        min_coordinate = np.min(coordinates)
        max_coordinate = np.max(coordinates)
        size = max_coordinate - min_coordinate
        assert size > 0
        all_sizes.append(size)
        all_coordinates.append(axis_coordinates)

    if dimensions == 2:
        all_names = ["x", "y"]
    elif dimensions == 3:
        all_names = ["u", "v", "w"]
    else:
        assert False

    order = np.argsort(all_sizes)
    for axis, name in zip(order, all_names):
        ut.set_o_data(adata, f"{prefix}{name}", all_coordinates[axis])


@ut.logged()
@ut.timed_call()
@ut.expand_doc()
def spread_coordinates(
    adata: AnnData,
    *,
    prefix: str = "",
    suffix: str = "_spread",
    cover_fraction: float = pr.spread_cover_fraction,
    noise_fraction: float = pr.spread_noise_fraction,
    random_seed: int,
) -> None:
    """
    Move UMAP points so they cover some fraction of the plot area without overlapping.

    **Input**

    The input annotated ``adata`` is expected to contain the per-observation properties
    ``<prefix>x`` and ``<prefix>y`` (default prefix: {prefix}) which contain the UMAP coordinates.

    **Returns**

    Sets the following annotations in ``adata``:

    Observation (Cell) Annotations
        ``<prefix>x<suffix>``, ``<prefix>y<suffix>`` (default suffix: {suffix})
            The new coordinates which will be spread out so the points do not overlap and
            cover some fraction of the total plot area.

    **Computation Parameters**

    1. Move the points so they cover ``cover_fraction`` (default: {cover_fraction}) of the total
       plot area. Also add a noise of the ``noise_fraction`` (default: {noise_fraction}) of the
       minimal distance between the points. A non-zero ``random_seed`` will make this reproducible.
    """
    assert 0 < cover_fraction < 1
    assert noise_fraction >= 0

    x_coordinates = ut.get_o_numpy(adata, f"{prefix}x")
    y_coordinates = ut.get_o_numpy(adata, f"{prefix}y")

    x_coordinates, y_coordinates = ut.cover_coordinates(
        x_coordinates,
        y_coordinates,
        cover_fraction=cover_fraction,
        noise_fraction=noise_fraction,
        random_seed=random_seed,
    )

    ut.set_o_data(adata, f"{prefix}x{suffix}", x_coordinates)
    ut.set_o_data(adata, f"{prefix}y{suffix}", y_coordinates)
