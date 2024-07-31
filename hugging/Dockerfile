# Use the official Python 3.10 image as the base image
FROM python:3.10

# install Git (if it's not already installed)
RUN apt-get update && apt-get install -y git

# force docker to rebuild from this step if version.json changes
ADD http://worldtimeapi.org/api/timezone/Asia/Jakarta version.json

# set timezone jakarta
ENV TZ=Asia/Jakarta

# git clone from private repo
RUN --mount=type=secret,id=GIT_REPO,mode=0444,required=true git clone $(cat /run/secrets/GIT_REPO) /repo

# install packages from packages.txt (apt-get install) using xargs
COPY /repo/packages.txt .
RUN xargs apt-get -y install < packages.txt

# allow permissions root folder
RUN cd ~ && chmod -R 777 .

# allow permissions this step
RUN chmod -R 777 .

# Install the Python dependencies
COPY /repo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the host machine to the working directory in the container
COPY /repo/ .

# Set the command to run when the container starts
# This command will start the Flask application
CMD ["python", "src/app.py"]

