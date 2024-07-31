# Use the official Python 3.10 image as the base image
FROM python:3.10

# install Git (if it's not already installed)
RUN apt-get update && apt-get install -y git

# force docker to rebuild from this step if version.json changes
ADD http://worldtimeapi.org/api/timezone/Asia/Jakarta version.json

# set timezone jakarta
ENV TZ=Asia/Jakarta

# git clone from private repo
RUN --mount=type=secret,id=GIT_REPO,mode=0444,required=true git clone $(cat /run/secrets/GIT_REPO) /app

# set working directory
WORKDIR /app

# install packages from packages.txt (apt-get install) using xargs
RUN xargs apt-get -y install < packages.txt

# give permission to root user
RUN chown -R root:root . && find . -type d -exec chmod 755 {} \; && find . -type f -exec chmod 644 {} \;

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy README.txt to /root
RUN cp README.txt /root

# Set the command to run when the container starts
# This command will start the Flask application
CMD ["python", "src/app.py"]

