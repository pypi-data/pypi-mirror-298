import pandas as pd

from dsp_pandas.df.missing_data import (
    decompose_NAs,
    get_record,
    percent_missing,
    percent_non_missing,
)


def test_percent_missing():
    df = pd.DataFrame({"A": [1, 2, None], "B": [None, 2, 3]})
    assert percent_missing(df) == 2 / 6


def test_percent_non_missing():
    df = pd.DataFrame({"A": [1, 2, None], "B": [None, 2, 3]})
    assert percent_non_missing(df) == 4 / 6


def test_get_record():
    df = pd.DataFrame({"A": [1, 2, None], "B": [None, 2, 3]})
    record = get_record(df)
    expected_record = {"N": 3, "M": 2, "N_obs": 4, "N_mis": 2, "missing": 2 / 6}
    assert record == expected_record


def test_decompose_NAs():
    df = pd.DataFrame(
        {"A": [1, None, None], "B": [None, 2, None], "C": [None, None, 3]},
        index=[1, 1, 2],
    )
    result = decompose_NAs(df, level=0)
    expected_result = pd.DataFrame(
        {
            "total_obs": [3],
            "total_MVs": [6],
            "real_MVs": [4],
            "indirectly_imputed_MVs": [2],
            "real_MVs_ratio": [4 / 6],
            "indirectly_imputed_MVs_ratio": [2 / 6],
            "total_MVs_ratio": [6 / 9],
        },
        index=["summary"],
    ).convert_dtypes()
    pd.testing.assert_frame_equal(result, expected_result)
