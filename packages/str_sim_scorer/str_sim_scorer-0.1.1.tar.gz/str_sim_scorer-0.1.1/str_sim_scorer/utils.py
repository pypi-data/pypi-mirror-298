from __future__ import annotations

import warnings
from itertools import combinations
from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from scipy import sparse


def collect_alleles(
    df: pd.DataFrame, id_col_name: str, locus_col_names: list[str]
) -> pd.DataFrame:
    """
    Given a data frame and the column names containing ID and STR loci, return a long
    data frame of unique alleles at observed loci for every ID.

    :param df: a data frame of STR profile data
    :param id_col_name: the name of the column containing an ID
    :param locus_col_names: the names of columns containing STR loci
    :return: a data frame of unique (ID, locus, allele) records
    """

    # get all alleles as a long data frame (one allele per profile-locus)
    alleles = df.melt(
        id_vars=[id_col_name],
        value_vars=locus_col_names,
        var_name="locus",
        value_name="allele",
    ).dropna()

    alleles = alleles.rename(columns={id_col_name: "id"})

    alleles = alleles.set_index(["id", "locus"])

    # make data frame of unique (ID, locus, allele) records
    alleles = (
        alleles["allele"]
        .str.extractall(r"(?P<allele>\d+(?:\.\d)?)")
        .reset_index()
        .drop(columns="match")
        .drop_duplicates()
        .sort_values(["id", "locus", "allele"])
        .reset_index(drop=True)
    )

    # use categories since this data frame and its derivations might be large
    alleles[["id", "locus", "allele"]] = alleles[["id", "locus", "allele"]].astype(
        "category"
    )

    return alleles


def count_overlaps(
    df: pd.DataFrame,
    pivot_index_cols: Iterable[str],
    id_col_name: str,
    overlap_col_name: str,
) -> pd.DataFrame:
    """
    Given a data frame with an ID column and some number of value columns, return a data
    frame giving the count of matching values for all possible pairs of IDs.

    :param df: a data frame with columns representing IDs and values to use for
    counting overlaps
    :param pivot_index_cols: name of columns containing values that jointly represent
    a value to use for counting overlaps
    :param id_col_name: name of column containing an ID
    :param overlap_col_name: name of column to use for the overlap size in the output
    :return: a data frame of IDs and counts of common values
    """

    # save the ID column categories
    id_cats = df[id_col_name].cat.categories

    # drop dups just in case
    df.drop_duplicates(subset=[id_col_name, *pivot_index_cols], inplace=True)

    # create indicator before pivoting into a sparse array
    df["present"] = True

    # pivot into wide data frame indicating presence of possible values at all locations
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        df = df.pivot(
            values="present", index=pivot_index_cols, columns=id_col_name
        ).notna()

    # convert to sparse matrix (id_col_name by pivot_index_cols)
    x = sparse.coo_array(df, dtype=np.ushort)

    # get symmetric matrix (ID by ID) of pairwise intersection set sizes
    x = x.transpose().dot(x)

    # we only need one of the triangulars to get every pair
    x = sparse.triu(x, k=1)

    # populate data frame with values and their row+col indexes in the sparse matrix
    x_df = pd.DataFrame({overlap_col_name: x.data})
    x_df.set_index([x.row, x.col], inplace=True)
    x_df.rename_axis(index=["r", "c"], inplace=True)

    # create empty data frame with all r/c combinations
    base_df = pd.DataFrame(combinations(range(0, x.shape[0]), r=2), columns=["r", "c"])
    base_df.set_index(["r", "c"], inplace=True)

    # fill data frame with the counts (or zeroes)
    x_df = base_df.join(x_df, how="left", on=["r", "c"])
    x_df[overlap_col_name].fillna(0, inplace=True)
    x_df[overlap_col_name] = x_df[overlap_col_name].astype("uint16")

    # create mapping between IDs and r/c values
    ids_df = pd.DataFrame({id_col_name: df.columns.tolist()})

    # join id1 values
    ids_df.rename_axis(index="r", inplace=True)
    x_df = x_df.join(ids_df, how="inner", on=["r"])

    # join id2 values
    ids_df.rename_axis(index="c", inplace=True)
    x_df = x_df.join(ids_df, how="inner", on=["c"], lsuffix="1", rsuffix="2")

    x_df.sort_index(inplace=True)

    # restore ID column categories
    id_col_names = [f"{id_col_name}1", f"{id_col_name}2"]
    x_df[id_col_names] = x_df[id_col_names].astype(
        pd.CategoricalDtype(categories=id_cats)
    )

    x_df.reset_index(drop=True, inplace=True)

    return x_df


def count_common_markers(alleles: pd.DataFrame) -> pd.DataFrame:
    """
    For all pairs of IDs in the `alleles` data frame, sum the number of alleles observed
    in both records, excluding loci that are observed in only one of them.

    :param alleles: a data frame of unique (ID, locus, allele) records
    :return: a data frame counting the number of alleles at loci common to pairs of IDs
    """

    # count the number of alleles per locus for each profile
    alleles_per_locus = (
        alleles[["id", "locus"]]
        .value_counts()
        .to_frame(name="n_alleles")
        .reset_index()
        .pivot(values="n_alleles", index="id", columns="locus")
    )
    alleles_per_locus = alleles_per_locus.fillna(0).astype("int")

    # save the row names for later
    ids = alleles_per_locus.index.tolist()

    # Minkowski addition gives us the pairwise sums of the rows
    m = np.array(alleles_per_locus)
    x = (m[:, None] + m).reshape(-1, m.shape[1])

    # construct another matrix of the same shape, but this time use 0/1 to indicate
    # which markers are present in both profiles for each pair
    m[m > 0] = 1
    xz = (m[:, None] * m).reshape(-1, m.shape[1])

    # sum the number of alleles in each pair, but only at markers where both profiles
    # had allele data
    nz_pair_combs = x * xz  # element-wise
    nz_pair_sums = np.sum(nz_pair_combs, axis=1)

    # collect the pairs of IDs for the `nz_pair_sums` array using the same
    # method to ensure the labels match the data
    ids_arr = np.array(ids, dtype=np.object_)
    id_pairs = (ids_arr[:, None] + "|" + ids_arr).reshape(-1)

    # convert to a long data frame and extract the two IDs
    common_markers = pd.DataFrame(nz_pair_sums, columns=["n_common_markers"])
    common_markers["ids"] = id_pairs
    common_markers[["id1", "id2"]] = common_markers["ids"].str.split("|", expand=True)
    common_markers = common_markers.drop(columns=["ids"])

    # we only need pairs where id1 < id2 (like in `count_shared_alleles`)
    common_markers = common_markers.loc[
        common_markers["id1"].lt(common_markers["id2"])
    ].reset_index(drop=True)

    common_markers[["id1", "id2"]] = common_markers[["id1", "id2"]].astype(
        pd.CategoricalDtype(categories=alleles["id"].cat.categories)
    )

    return common_markers


def compute_tanabe_scores(
    shared_alleles: pd.DataFrame, common_markers: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute the Tanabe score for pairs of IDs, given previously-calculated counts of
    shared alleles and common markers.

    :param shared_alleles: a data frame counting the number of shared alleles at loci
    common to pairs of IDs
    :param common_markers: a data frame counting the number of alleles at loci common to
    pairs of IDs
    :return: a data frame with Tanabe scores for pairs of IDs
    """

    # use common_markers as a base data frame, join the shared alleles (when available)
    tanabe_scores = common_markers.merge(shared_alleles, how="left", on=["id1", "id2"])

    # if `n` is NA in row id1-id2, then we know we have that data elsewhere as id2-id1
    tanabe_scores = tanabe_scores.dropna(subset="n_shared_alleles")

    tanabe_scores["n_shared_alleles"] = tanabe_scores["n_shared_alleles"].astype("int")
    tanabe_scores["tanabe"] = (
        2 * tanabe_scores["n_shared_alleles"] / tanabe_scores["n_common_markers"]
    )

    return tanabe_scores


def reflect_tanabe_scores(tanabe_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Given a data frame of Tanabe scores for records like (id1, id2, score), append rows
    like (id2, id1, score).

    :param tanabe_scores: a data frame with Tanabe scores for pairs of IDs
    :return: a data frame of Tanabe scores with rows for both (id1, id2) and (id2, id1)
    pairs
    """

    tanabe_scores_reflect = tanabe_scores.copy()
    tanabe_scores_reflect[["id1", "id2"]] = tanabe_scores_reflect[["id2", "id1"]]

    return pd.concat([tanabe_scores, tanabe_scores_reflect], ignore_index=True)


def scores_df_to_np(tanabe_scores: pd.DataFrame) -> Tuple[np.ndarray, list[str]]:
    """
    Convert the symmetric Tanabe scores data frame to a numpy array

    :param tanabe_scores: a data frame of Tanabe scores
    :return: a symmetric numpy array and a list of IDs corresponding to the row and
    column names
    """

    symm_df = tanabe_scores.set_index(["id1", "id2"])["tanabe"].unstack()

    arr = symm_df.values
    arr = np.triu(arr) + np.triu(arr, 1).T
    np.fill_diagonal(arr, 1)

    return arr, symm_df.columns.tolist()
