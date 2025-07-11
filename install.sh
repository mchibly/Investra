#!/usr/bin/env bash

# This script installs Docker on Amazon Linux and runs the fundamentus scraper
# inside a container.

set -euo pipefail

# Install Docker
sudo yum update -y
sudo amazon-linux-extras install docker -y || sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker $USER

# Build the Docker image
sudo docker build -t fundamentus-scraper .

# Run the scraper
sudo docker run --rm fundamentus-scraper
