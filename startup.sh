#!/bin/bash
# Install ffmpeg if not available
apt-get update
apt-get install -y ffmpeg

# Start the application with gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 application:application
