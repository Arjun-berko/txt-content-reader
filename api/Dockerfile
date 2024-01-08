# Using official Python runtime as a parent image
FROM python:3.8

# Setting working directory within container
WORKDIR /usr/src/app

# Copying the current directory contents into the container at /usr/src/app
COPY . .

# Installing the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Making port 8000 available outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
