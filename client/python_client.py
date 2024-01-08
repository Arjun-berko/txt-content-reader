import requests

# FastAPI application URL
url = 'http://127.0.0.1:8000/upload-file/'

# Path to desired file
file_path = 'sample.txt'

try:
    # Opening file and sending it through POST request
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': (file_path, file, 'text/plain')})

        # Checking response status code and printing appropriate message
        if response.status_code == 200:
            print("File uploaded successfully. Response:")
            print(response.json())
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print(response.json())

except IOError as e:
    # showing error arising fron not being able to access text file
    print(f"Error opening file: {e}")
