import pytest
from main import valid_report
from main import valid_date
from main import read_files
from main import Handling
list_of_reports = ["average"]
def test_invalid_report():
    with pytest.raises(ValueError):
        valid_report("another",list_of_reports)

def test_valid_report():
    valid_report("average",list_of_reports)

def test_invalid_date():
    with pytest.raises(ValueError):
        valid_date("202211122")

def test_valid_date():
    valid_date("2025-10-12")

def test_read_files_error():
    with pytest.raises(FileNotFoundError):
        read_files(["example1","example3"])

def test_read_files():
    read_files(["example1.log","example2.log"])

def test_Handling():
    example_report = [{"handler":"/api/context/...", "total":2, "avg_response_time":0.02},{"handler":"/api/homeworks/...", "total":2, "avg_response_time":0.05}]
    objects = read_files(["example3.log"])
    report = Handling(objects, "average", "none")
    assert report == example_report