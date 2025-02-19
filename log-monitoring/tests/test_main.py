import pytest
from unittest.mock import mock_open, patch, MagicMock
from ..main import (
    time_diff_in_seconds,
    is_warining,
    is_error,
    analy_log,
)

@pytest.mark.parametrize("start_at, end_at, expected", [
    ("10:11:12", "10:11:15", 3),
    ("0:01:0", "0:2:5", 65),
    ("1:01:0", "2:2:1", 3661),
])
def test_time_diff_in_seconds(start_at, end_at, expected):
    assert time_diff_in_seconds(start_at, end_at) == expected

@pytest.mark.parametrize("start_at, end_at, expected", [
    ("10:11:12", "10:11:15", False),
    ("0:01:0", "0:8:0", True),
    ("0:01:0", "0:6:0", True),
    ("0:01:0", "0:11:0", False),
    ("1:01:0", "2:2:1", False),
])
def test_is_warining(start_at, end_at, expected):
    """
    Time diff more than or equal to 5 mins and less than 10 mins
    """
    assert is_warining(start_at, end_at) == expected

@pytest.mark.parametrize("start_at, end_at, expected", [
    ("10:11:12", "10:11:15", False),
    ("0:01:0", "0:8:0", False),
    ("0:01:0", "0:6:0", False),
    ("0:01:0", "0:11:0", True),
    ("1:01:0", "2:2:1", True),
])
def test_is_error(start_at, end_at, expected):
    """
    Time diff more than 10 mins
    """
    assert is_error(start_at, end_at) == expected


def test_analy_log():
    # Mock CSV data
    mock_csv_data = "11:35:23,scheduled task 032, START,37980\n" + \
        "11:35:56,scheduled task 032, END,37980\n" + \
        "11:38:23,scheduled task 038, START,67980\n" + \
        "11:45:56,scheduled task 038, END,67980\n" + \
        "11:50:11,scheduled task 796, START,57672\n" + \
        "11:55:18,scheduled task 796, PROCESS,57672\n" + \
        "12:36:58,background job wmy, END,57672\n" + \
        "20:37:14,scheduled task 515, START,45135\n" + \
        "30:37:14,scheduled task 515, END,45135\n"

    # Mock open and csv.reader
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        with patch("os.path.exists", return_value=True):
            with patch("csv.reader") as mock_csv_reader:
                # Set up the mock csv.reader to return specific rows
                mock_csv_reader.return_value = [
                    ["11:35:23", "scheduled task 032", "START", "37980"],
                    ["11:35:56", "scheduled task 032", "END", "37980"],
                    ["11:38:23", "scheduled task 038", "START", "67980"],
                    ["11:45:56", "scheduled task 038", "END", "67980"],
                    ["11:50:11", "scheduled task 796", "START", "57672"],
                    ["11:55:18", "scheduled task 796", "PROCESS", "57672"],
                    ["12:36:58", "background job wmy", "END", "57672"],
                    ["20:37:14", "scheduled task 515", "START", "45135"],
                    ["30:37:14", "scheduled task 515", "END", "45135"],
                ]

                # Call the function
                result = analy_log("test.csv")
                assert result.total_records == 8
                assert result.error_records == 1
                assert result.warning_records == 1
                assert result.exception_records == 1
                assert result.start_without_end_records == 1