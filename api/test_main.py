from fastapi.testclient import TestClient
import pytest
from main import process_text
from main import app, cache
import os

client = TestClient(app)


def test_upload_file():
    """
    Test the file upload endpoint with a sample text file.

    This test checks if the endpoint correctly handles a file upload
    and returns the expected status code and response.
    """
    # Create a test file with sample content
    with open("test.txt", "wb") as file:
        file.write(b"test content")

    # Test the file upload
    with open("test.txt", "rb") as file:
        response = client.post("/upload-file/", files={"file": file})
        assert response.status_code == 200


def test_process_text():
    """
    Test the process_text function with a sample string.

    This test ensures that the process_text function returns
    the correct word count for a given string.
    """
    # Encoding the string into bytes for processing
    content = "Sample text for testing.".encode("utf-8")
    result = process_text(content)

    assert result["word_count"] == 4


def test_upload_file_caching():
    """
    Test the caching functionality of the file upload endpoint.

    This test ensures that the endpoint correctly caches the results
    of file uploads to avoid unnecessary processing.
    """
    # Clear the cache before running the test
    cache.clear()

    try:
        # Create and write to a test file
        with open("test.txt", "w") as file:
            file.write("test content")

        # First upload (should not be cached)
        with open("test.txt", "rb") as file:
            response_1 = client.post("/upload-file/", files={"file": ("test.txt", file)})
            assert response_1.status_code == 200
            assert "cached" in response_1.json() and response_1.json()["cached"] is False

        # Second upload (should be cached)
        with open("test.txt", "rb") as file:
            response_2 = client.post("/upload-file/", files={"file": ("test.txt", file)})
            assert response_2.status_code == 200
            assert "cached" in response_2.json() and response_2.json()["cached"] is True

    finally:
        # Cleanup to remove the test file after the test
        os.remove("test.txt")


