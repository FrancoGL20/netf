import sys
import pytest
from pathlib import Path
import shutil

# Get the path to the current test directory
TEST_PATH = Path(__file__).parent

# Add the project root to sys.path for imports
sys.path.insert(0, TEST_PATH.parent.as_posix())

from src.utils.xml_files_processing import map_ids

@pytest.fixture
def clean_output_dir():
    """
    Fixture to clean the output directory before each test.
    """
    output_dir = TEST_PATH / "test_files/xml_mapping/test_output"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    yield output_dir
    shutil.rmtree(output_dir)

def test_xml_file_mapping(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows.
    - file_with_mapping: file with the correct columns to map.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir
    )
    assert result == (409, 409, 0)


def test_xml_file_mapping_with_unmap(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows unmapped.
    - file_with_mapping: file with the correct columns to map.
    - unmap: True to unmap the file_to_map.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_002.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        unmap=True
    )
    assert result == (409, 409, 0)


def test_xml_file_mapping_with_unmap_true_when_file_is_not_unmapped(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows not mapped.
    - file_with_mapping: file with the correct columns to map.
    - unmap: True to unmap the file_to_map, but as the file is not mapped, it should 0 mapped and all rows as errors.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        unmap=True
    )
    assert result == (409, 0, 409)


def test_xml_file_mapping_with_has_details(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows and has_details.
    - file_with_mapping: file with the correct columns to map.
    - has_details: True to skip the detail rows.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_003.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        has_details=True
    )
    assert result == (409, 409, 0)


def test_xml_file_mapping_with_columns_to_map(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows.
    - file_with_mapping: file with the correct columns to map.
    - columns_to_map: specific column to map.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        columns_to_map="Tariff ID"
    )
    assert result == (409, 409, 0)


def test_xml_file_mapping_with_columns_to_map_list(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows.
    - file_with_mapping: file with the correct columns to map.
    - columns_to_map: list of columns to map.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        columns_to_map=["Tariff ID", "Tariff Number"]
    )
    assert result == (409, 409, 0)


def test_xml_file_mapping_with_columns_to_map_list_error(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows.
    - file_with_mapping: file with the correct columns to map.
    - columns_to_map: list with columns to map that are not in the file, so it should return an error.
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_001_correct.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir,
        columns_to_map=["Tariff IDs", "Tariff Number", "Tariff Code"]
    )
    assert result == "None of the columns to map were found in the file"


def test_xml_file_mapping_with_mapping_file_error(clean_output_dir):
    """
    Test file mapping with:
    - file_to_map: file with the H and D struture of rows.
    - file_with_mapping: file with a mapping file with the wrong columns (neither Tariff ID nor Tariff Number).
    """
    file_with_mapping = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_mapping_file_002_incorrect.xlsx"
    file_to_map = TEST_PATH / "test_files/xml_mapping/test_xml_mapping_input_001.xml"
    output_dir = clean_output_dir.as_posix()
    result = map_ids(
        file_with_mapping=file_with_mapping.as_posix(),
        file_to_map=file_to_map.as_posix(),
        dir_output=output_dir
    )
    assert result == "The mapping file does not have the expected columns ['Tariff ID', 'Tariff Number']"
