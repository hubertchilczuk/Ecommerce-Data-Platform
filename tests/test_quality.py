from data_quality.checks import check_no_nulls, check_non_negative, check_unique


def test_check_no_nulls_passes():
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    assert check_no_nulls(rows, ["a", "b"]).passed


def test_check_no_nulls_fails():
    rows = [{"a": 1, "b": None}]
    assert not check_no_nulls(rows, ["a", "b"]).passed


def test_check_non_negative():
    assert check_non_negative([{"x": 0}, {"x": 5}], "x").passed
    assert not check_non_negative([{"x": -1}], "x").passed


def test_check_unique():
    assert check_unique([{"id": 1}, {"id": 2}], "id").passed
    assert not check_unique([{"id": 1}, {"id": 1}], "id").passed
