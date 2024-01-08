import hashlib
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from collections import Counter
from fastapi.responses import JSONResponse
import re

app = FastAPI()

class TextModel(BaseModel):
    """
    This class is the data model for text input.
    It includes a single field 'text' which is a string.
    """
    text: str

def process_text(content: bytes) -> dict:
    """
    Process the text from the files to calculate various statistics.

    The function performs regex pattern matching to extract words, email addresses,
    dates, URLs, currency amounts, and standalone ampersands. It then calculates
    the total word count, average word length, distribution of word lengths, and
    the most frequently occurring word lengths.

    Args:
    content (bytes): The text content to be processed.

    Returns:
    dict: A dictionary containing the calculated statistics.
    """
    # Regex pattern to match different elements in the text
    words = re.findall(
        r'''
        [\w\-\'.]+\@[\w\-\']+\.[\w\-\']+|  # Email addresses with dot in the username
        \b\d{1,2}/\d{1,2}/\d{2,4}\b|      # Dates in dd/mm/yyyy format
        \b\d{1,2}-\d{1,2}-\d{2,4}\b|      # Dates in dd-mm-yyyy format
        \bhttps?:\/\/[\w\-\'.\/]+|        # URLs including http, https, periods, and slashes
        \b[\w\-\']+|                      # Words with alphanumeric characters, hyphens, and apostrophes
        [£$€]\d+(?:,\d{3})*(?:\.\d+)?\b|  # Currency amounts
        &                                 # Ampersand as a standalone word
        ''', content.decode("utf-8"), re.VERBOSE)



    word_lengths = [len(word) for word in words]
    total_word_count = len(word_lengths)
    average_word_length = round(sum(word_lengths) / total_word_count, 2) if total_word_count > 0 else 0.0

    # Count the occurrences of each word length
    word_length_counts = Counter(word_lengths)

    # Find the most frequent word length(s)
    max_frequency = max(word_length_counts.values(), default=0)
    most_common_lengths = [length for length, freq in word_length_counts.items() if freq == max_frequency]

    # Order the word length distribution by increasing word length
    ordered_word_length_distribution = {k: v for k, v in sorted(word_length_counts.items(), key=lambda item: item[0])}

    return {
        "word_count": total_word_count,
        "average_word_length": average_word_length,
        "word_length_distribution": ordered_word_length_distribution,
        "most_frequently_occurring_word_lengths": most_common_lengths,
        "number_of_occurrences": max_frequency
    }

# Initialise the cache dictionary
cache = {}

@app.post("/upload-file/")
async def count_words_in_file(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to upload a text file and get statistics on the words contained.

    This endpoint accepts only plain text files. It reads the file's content, processes it
    to calculate various statistics like word count, average word length, etc., and returns these statistics.
    It uses an MD5 checksum to cache and retrieve results for previously processed files,
    which improves performance and avoids unnecessary processing.

    Args:
    file (UploadFile): The text file to be uploaded.

    Returns:
    JSONResponse: A JSON response containing the text statistics or an error message.
    """
    # Check if the uploaded file is a plain text file
    if file.content_type != 'text/plain':
        return JSONResponse(
            status_code=400,
            content={"message": "Unsupported file format. Please upload a .txt file."}
        )

    # Reading file contents and handling file read errors
    try:
        content = await file.read()
    except IOError as io_error:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error reading file: {str(io_error)}"}
        )

    try:
        # Calculating the MD5 checksum of the file content for caching
        checksum = hashlib.md5(content).hexdigest()

        # Checking if result is already in the cache
        if checksum in cache:
            cached_data = cache[checksum]
            return {**cached_data, "cached": True}

        # Processing the text and storing result in cache
        processed_text = process_text(content)
        cache[checksum] = processed_text
        return {**processed_text, "cached": False}

    except Exception as e:
        # Displaying the exception to be used for debugging
        return JSONResponse(
            status_code=500,
            content={"message": f"An internal error occurred: {str(e)}"}
        )

