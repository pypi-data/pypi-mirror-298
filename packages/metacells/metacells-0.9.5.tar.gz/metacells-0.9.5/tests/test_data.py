"""
Test applying functions to real data.
"""

import logging
from glob import glob
from typing import Any
from typing import Dict
from typing import Tuple

import numpy as np
import scanpy as sc  # type: ignore
import yaml  # type: ignore
from anndata import AnnData  # type: ignore

import metacells as mc

# pylint: disable=missing-function-docstring

np.seterr(all="raise")
mc.ut.setup_logger(level=logging.WARN)
mc.ut.allow_inefficient_layout(False)
mc.ut.set_processors_count(4)

LOADED: Dict[str, Tuple[AnnData, Dict[str, Any]]] = {}


def _load(path: str) -> Tuple[AnnData, Dict[str, Any]]:
    if path in LOADED:
        return LOADED[path]

    with open(path[:-4] + "yaml", encoding="utf8") as file:
        expected = yaml.safe_load(file)
    with mc.ut.timed_step("read"):
        adata = sc.read(path)

    LOADED[path] = (adata, expected)
    mc.ut.set_name(adata, path.split("/")[-1][:-5])
    return adata, expected


def test_find_rare_gene_modules() -> None:
    for path in glob("../metacells-test-data/*.h5ad"):
        adata, expected = _load(path)

        mc.pl.mark_lateral_genes(adata, **expected.get("mark_lateral_genes", {}))
        mc.tl.find_rare_gene_modules(  #
            adata,
            reproducible=True,
            **expected.get("find_rare_gene_modules", {}),
        )

        actual_rare_gene_modules = []
        rare_gene_modules = mc.ut.get_v_numpy(adata, "rare_gene_module")
        max_gene_module = np.max(rare_gene_modules)
        for module_index in range(max_gene_module + 1):
            actual_rare_gene_modules.append(sorted(adata.var_names[rare_gene_modules == module_index]))

        expected_rare_gene_modules = expected["rare_gene_modules"]
        assert actual_rare_gene_modules == expected_rare_gene_modules


def test_direct_pipeline() -> None:
    for path in glob("../metacells-test-data/*.h5ad"):
        adata, expected = _load(path)

        mc.ut.log_calc("path", path)
        pdata = adata[range(6000), :].copy()

        mc.pl.exclude_genes(pdata, random_seed=123456, **expected.get("exclude_genes", {}))
        mc.pl.exclude_cells(pdata, **expected.get("exclude_cells", {}))
        cdata = mc.pl.extract_clean_data(pdata)
        assert cdata is not None

        mc.pl.mark_lateral_genes(pdata, **expected.get("mark_lateral_genes", {}))

        mc.pl.compute_direct_metacells(cdata, random_seed=123456, **expected.get("compute_direct_metacells", {}))

        mdata = mc.pl.collect_metacells(cdata, random_seed=123456)

        mc.pl.compute_for_mcview(adata=cdata, gdata=mdata, random_seed=123456)

        expected_results = expected["inner_stdev_log"]

        actual_results = np.mean(
            mc.ut.to_numpy_matrix(mc.ut.get_vo_proper(mdata, "inner_stdev_log", layout="column_major"))
        )

        # mc.ut.log_calc('PATH', path)
        # mc.ut.log_calc('EXPECT', expected_results)
        # mc.ut.log_calc('ACTUAL', actual_results)
        assert np.allclose([expected_results], [actual_results])
