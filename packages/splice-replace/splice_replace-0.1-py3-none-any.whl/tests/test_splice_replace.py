import pytest
import os
from splice_replace.splice_replace import extract_text, replace_text_in_file

# Test data setup
TEST_FILE = 'test_file.txt'

@pytest.fixture
def setup_file():
    """Create a temporary file for testing."""
    with open(TEST_FILE, 'w') as f:
        f.write("This is the first line.\n")
        f.write("This is the second line.\n")
        f.write("This is the third line.\n")
        f.write("This is the fourth line.\n")
        f.write("This is the fifth line.\n")
        f.write("1234567890123456789012345\n")
    yield
    os.remove(TEST_FILE)

def test_extract_text(setup_file):
    """Test extracting text from the file."""
    # Test extracting from a single line
    result = extract_text(TEST_FILE, 1, 12, 1, 18)  # Extract "second"
    assert result == "second"

    # Test extracting across multiple lines
    result = extract_text(TEST_FILE, 0, 5, 1, 8)  # Extract "is the se" + "this is t"
    assert result == "is the first line.\nThis is "


def test_replace_text_in_file(setup_file):
    """Test replacing text in the file."""
    replace_text_in_file(TEST_FILE, 1, 12, 1, 18, "changed")  # Replace "the sec" with "changed"

    with open(TEST_FILE, 'r') as f:
        lines = f.readlines()

    # Check if the replacement was successful
    assert lines[1] == "This is the changed line.\n"


def test_edge_cases(setup_file):
    """Test edge cases for text extraction and replacement."""
    # Test extracting with start and end on the same line
    result = extract_text(TEST_FILE, 4, 8, 4, 13)  # Extract "the f"
    assert result == "the f"

    # Test replacing with empty string
    replace_text_in_file(TEST_FILE, 0, 0, 0, 4, "")  # Replace "This" with ""
    with open(TEST_FILE, 'r') as f:
        lines = f.readlines()

    assert lines[0] == " is the first line.\n"

def test_multiple_lines(setup_file):
    """Test extracting and replacing text across multiple lines."""
    # Test extracting and replacing across multiple lines
    replace_text_in_file(TEST_FILE, 1, 0, 3, 0, "INSERTION\n")  # Replace lines 2-4
    with open(TEST_FILE, 'r') as f:
        lines = f.readlines()

    # Check if the replacement was successful
    assert lines[0] == "This is the first line.\n"
    assert lines[1] == "INSERTION\n"
    assert lines[2] == "This is the fourth line.\n"
    assert lines[3] == "This is the fifth line.\n"
    assert lines[4] == "1234567890123456789012345\n"