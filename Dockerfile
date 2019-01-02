
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["gunicorn", "-e", "SCRIPT_NAME=/applist", "-b", "0.0.0.0:5000", "index:app"]