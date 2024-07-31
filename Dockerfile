# Use the official Python 3.10 image as the base image
FROM python:3.10

# update & upgrade packages
RUN apt-get update && apt-get upgrade -y

# give permission to root user
RUN chown -R root:root . && find . -type d -exec chmod 755 {} \; && find . -type f -exec chmod 644 {} \;

# install packages from packages.txt (apt-get install) using xargs
COPY packages.txt .
RUN xargs apt-get -y install < packages.txt

# Copy all the files from the host machine to the working directory in the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app


RUN pip install --no-cache-dir -r requirements.txt

# copy README.txt to /root
RUN cp README.txt /root

# Set the command to run when the container starts
# This command will start the Flask application
CMD ["python", "src/app.py"]

