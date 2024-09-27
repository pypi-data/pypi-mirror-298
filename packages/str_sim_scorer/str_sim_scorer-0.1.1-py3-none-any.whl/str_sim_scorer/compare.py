from __future__ import annotations

from typing import Literal, Tuple

import numpy as np
import pandas as pd

from str_sim_scorer.utils import (
    collect_alleles,
    compute_tanabe_scores,
    count_common_markers,
    count_overlaps,
    reflect_tanabe_scores,
    scores_df_to_np,
)


def compare(
    df: pd.DataFrame,
    id_col_name: str,
    locus_col_names: list[str],
    output: Literal["df", "symmetric_df", "array"],
) -> pd.DataFrame | Tuple[np.ndarray, list[str]]:
    """
    Given a data frame containing STR profile data and column name information, compute
    the Tanabe score ("non-empty markers" mode) for all pairs of records.

    :param df: a data frame of STR profile data
    :param id_col_name: the name of the column containing a sample/profile/patient ID
    :param locus_col_names: the names of columns containing STR loci
    :param output: the output format requested (data frame, symmetric data frame, array)
    :return: a data frame of Tanabe scores, or an array of Tanabe scores along with its
    row/column names (the IDs)
    """

    # get long data frame of unique (ID, locus, allele) records
    alleles = collect_alleles(df, id_col_name, locus_col_names)

    # count alleles shared by pairs of IDs
    shared_alleles = count_overlaps(
        alleles,
        pivot_index_cols=["locus", "allele"],
        id_col_name="id",
        overlap_col_name="n_shared_alleles",
    )

    # sum markers at common loci for all pairs of IDs
    common_markers = count_common_markers(alleles)

    # compute the Tanabe score (non-empty markers ode)
    tanabe_scores = compute_tanabe_scores(shared_alleles, common_markers)

    if output != "df":
        # duplicate rows for (id1, id2) scores as (id2, id1)
        tanabe_scores = reflect_tanabe_scores(tanabe_scores)

    if output == "array":
        # return as a symmetric array along with its row/column names (the IDs)
        return scores_df_to_np(tanabe_scores)

    # use original id column name format and reorder columns
    tanabe_scores = tanabe_scores.rename(
        columns={"id1": f"{id_col_name}1", "id2": f"{id_col_name}2"}
    )[
        [
            f"{id_col_name}1",
            f"{id_col_name}2",
            "n_shared_alleles",
            "n_common_markers",
            "tanabe",
        ]
    ]

    return tanabe_scores
