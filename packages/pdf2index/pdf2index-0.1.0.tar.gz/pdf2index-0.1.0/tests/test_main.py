from pdf2index import __main__ as main
import pytest
import shutil
from pathlib import Path

TEST_DIR = "test_dir"
TEST_FILE = f"{TEST_DIR}/test_index.txt"


@pytest.fixture
def setup_test():
    shutil.rmtree(TEST_DIR, ignore_errors=True)
    Path(TEST_DIR).mkdir(parents=True, exist_ok=True)


def assert_test_index():
    with open(TEST_FILE) as f:
        index = f.read()
    with open("data/test_index.txt") as f:
        index_exp = f.read()
    assert index == index_exp


def test_main_without_password(setup_test):
    main.main(
        [
            "data/nopasswd/Book 1 - Lightweight_Directory_Access_Protocol.pdf",
            "data/nopasswd/Book 2 - Single_sign-on.pdf",
        ],
        out=TEST_FILE,
    )
    assert_test_index()


def test_main_with_password(setup_test):
    main.main(
        ["data/passwd/Book 1 - Lightweight_Directory_Access_Protocol.pdf", "data/passwd/Book 2 - Single_sign-on.pdf"],
        out=TEST_FILE,
        password="testpassword",
    )
    assert_test_index()
