import pytest
from project import isValid
from project import sortAlphabetical
from project import readList
import csv


def test_isValid():
    assert isValid("xxx.csv") == True
    assert isValid("xAx") == False
    assert isValid("xx78hgv.docx") == True
    assert isValid("xx78hgv") == False
    assert isValid("xx78hgv.txt") == True
    assert isValid("xx78hgv.txt.pdf") == True
    assert isValid("xx78hgv.pdf.txt") == True
    assert isValid("xx78hgv.xls") == True
    assert isValid("xx78hgv.xlsx") == True
    assert isValid(".csv") == True
    assert isValid("csv") == False


def test_sortAlphabetical():
    wl1 = [["apple", ""], ["kiwi", ""], ["zebra", ""], ["read", ""], ["altittude", ""]]
    wl = [
        ["altittude", ""],
        ["apple", ""],
        ["kiwi", ""],
        ["read", ""],
        ["zebra", ""],
    ]
    wl2 = [["kiwi", ""], ["read", ""], ["altittude", ""], ["apple", ""], ["zebra", ""]]
    assert sortAlphabetical(wl1) == wl
    assert sortAlphabetical(wl2) == wl


def test_read_csv():
    vocab = [
        ["apple", "苹果"],
        ["banana", "香蕉"],
        ["rest", "休息/剩余"],
        ["think", "思考"],
        ["sink", "下沉"],
    ]
    tempFile = "temp_file.csv"
    with open(tempFile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(vocab)
    result = readList(tempFile)
    assert result == vocab


# from an empty csv file return empty list
def test_read_empty_csv():
    csv_file = "empty.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow("")
    result = readList(csv_file)
    assert result == [[]]
