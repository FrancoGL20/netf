import sys
import pytest
from pathlib import Path
import shutil

# Get the path to the current test directory
TEST_PATH = Path(__file__).parent

# Add the project root to sys.path for imports
sys.path.insert(0, TEST_PATH.parent.as_posix())

from src.utils.files_processing import drop_duplicates

@pytest.fixture
def clean_output_dir():
    """
    Fixture to clean the output directory before each test.
    """
    output_dir = TEST_PATH / "test_files/drop_duplicates/test_output"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    yield output_dir
    shutil.rmtree(output_dir)

def test_drop_duplicates_without_end_enter(clean_output_dir):
    """
    Test drop_duplicates with a file that does not end with a newline (last line does not end with a newline).
    """
    input_filename = TEST_PATH / "test_files/drop_duplicates/test_drop_duplicates_input01.txt"
    output_filename = input_filename.name

    original_no_lines, new_no_lines = drop_duplicates(
        input_filename.as_posix(),
        output_filename,
        clean_output_dir.as_posix()
    )

    with open(clean_output_dir / output_filename, "r", encoding="utf-8") as f:
        output = f.read()
        assert output == "info\nmodule\nof\nreview\ntest_drop_duplicates\nthe\nto\nwith\n"
        assert original_no_lines == 20
        assert new_no_lines == 8

def test_drop_duplicates_with_end_enter(clean_output_dir):
    """
    Test drop_duplicates with a file that ends with a newline (last line ends with a newline).
    """
    input_filename = TEST_PATH / "test_files/drop_duplicates/test_drop_duplicates_input02.txt"
    output_filename = input_filename.name

    original_no_lines, new_no_lines = drop_duplicates(
        input_filename.as_posix(),
        output_filename,
        clean_output_dir.as_posix()
    )

    with open(clean_output_dir / output_filename, "r", encoding="utf-8") as f:
        output = f.read()
        assert output == "info\nmodule\nof\nreview\ntest_drop_duplicates\nthe\nto\nwith\n"
        assert original_no_lines == 20
        assert new_no_lines == 8