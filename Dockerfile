
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl -o dockerize-linux-amd64-v0.6.1.tar.gz https://raw.githubusercontent.com/kbase/dockerize/master/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xvzf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENTRYPOINT [ "/usr/local/bin/dockerize" ]
CMD [ "sh", "scripts/start_server.sh"]