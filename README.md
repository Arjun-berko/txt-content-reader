# README for FastAPI Text Processing Application

## Description

This FastAPI application is designed to process text files uploaded by users. It analyses the text content, extracting information such as word count, average word length, number of words of each word length, and the frequency of the most common word lengths. The application uses regex pattern matching to identify various elements in the text like words, email addresses, dates, URLs, currency amounts, and standalone ampersands. Caching has been implemented using checksums to improve performance by avoiding unnecessary repeated processing of the same files.

## Edge-cases: what counts as a word?

The following edge-cases have been counted as a single word:
- Regular words such as "apple" or "Hertfordshire", separated by whitespaces
- Date patterns such as 12/02/2023 or 12-02-2023
- Email IDs, such as arjun1234@gmail.com, with characters like dots or underscores in them
- URLs, such as https://www.google.co.uk/
- Currency signs shown with numbers, such as £12 or $30
- Ampersands (&) used instead of the word "and"
- Words that contain numbers, hyphens or apostrophes within them, such as "23rd", "it's" or "edge-cases"
 
## Features

- **Text Analysis**: Calculates word count, average word length, and word length distribution.
- **Word Recognition**: Identifies emails, dates, URLs, currencies, and decides whether they count as word or not based on edge-case assumptions specified above.
- **Caching**: Uses checksums to cache results of previously processed files.

## Prerequisites

Before you begin, ensure that you have Docker and GIT installed on your computer.

## Setup and Installation

1. **Clone the Repository**
   
   First, clone the repository to your local machine and then enter it using the following terminal commands:

   ```bash
   git clone https://github.com/Arjun-berko/txt-content-reader
   cd txt-content-reader
   ```
2. **Build the Docker Image**
   
   Inside the repository, navigate to the "api" directory and build the docker image:

   ```bash
   cd api
   docker build -t txt-reader-app .
   ```
   This command builds a Docker image named txt-reader-app based on the Dockerfile in the current directory.


3. **Run the Docker Container**
   
   Once the image is built, you can run the container:

   ```bash
   docker run -d -p 8000:8000 --name txt-reader-container txt-reader-app
   ```
   This command runs the container in detached mode, maps port 8000 of the container to port 8000 of the host, and names the container txt-reader-container.
   
   Please note, after this point, you can stop and start the container using the following commands, which are more straightforward:

   ```bash
   docker stop txt-reader-container
   docker start txt-reader-container
   ```


## Usage

   - Once the application is running, you can access it through your browser or API client at http://localhost:8000.
   - Uploading a File: Use the /upload-file/ endpoint to upload a text file and receive the analysis results as JSON data.
### Testing
   The app has a test file that contains unit tests, called `test_main.py`. These are used to test the regex text processing function, the file upload endpoint, and the caching capabilities of the app. To run these tests, run the following command while the container is running:
   ```bash
   docker exec txt-reader-container pytest
   ```

### Client
   - This repository also provides a Python-based client for the user to test the app, along with a sample .txt file. To use this, first run the Docker container to start the API server. Then, open a separate terminal window and navigate into the "client" folder within the root directory.
   ```bash
   cd ..
   cd client
   ```
   - Open the `sample.txt` file add any text you want. Alternatively, you can open the Python client file and change the `file_path` variable to the path to your desired .txt file. Then, run the client file using the following command:
   ```bash
   python3 client.py
   ```
   - This should display the JSON data regarding the word statistics of the `.txt` file in the terminal.
   - Alternatively, use an API request service such as Insomnia or Postman.