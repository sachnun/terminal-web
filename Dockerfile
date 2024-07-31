# Use the official Python 3.10 image as the base image
FROM python:3.10

# update & upgrade packages
RUN apt-get update && apt-get upgrade -y

# install packages from packages.txt (apt-get install) using xargs
COPY packages.txt .
RUN xargs apt-get -y install < packages.txt

# Set the working directory inside the container
WORKDIR /app

# allow permissions
RUN chmod -R 777 .

# allow permissions workdir
RUN chmod -R 777 /app

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the host machine to the working directory in the container
COPY . .

# copy README.txt to /root
COPY README.txt /root

# Set the command to run when the container starts
# This command will start the Flask application
CMD ["python", "src/app.py"]

