# Use the Ubuntu 22.04 (or your desired version) as the base image
FROM ubuntu:22.04

# Set the maintainer label (replace with your information)
LABEL maintainer="nasserjamal30@email.com"

# Update package lists and install any necessary packages
RUN apt-get update && apt-get install -y \
    # Add the packages you need here, e.g., nano, curl, etc.
    nano \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all files and folders from the current directory into the container
COPY . /app

# Expose ports 3000 and 8000
EXPOSE 3000
EXPOSE 8000

# Specify any additional commands or entry point for your container
# CMD ["/your/command"]

# You may add more instructions as needed for your specific application
# docker build -t my-ubuntu-image .
# docker run -it -p 3000:3000 -p 8000:8000 my-ubuntu-image
