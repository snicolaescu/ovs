#!/bin/bash

# Variables that I will move to Params~
USER_NAME=`echo $DRONE_BUILD_DIR| cut -d'/' -f 7`
REPO_NAME=`echo $DRONE_BUILD_DIR| cut -d'/' -f 8`
BASE_PORT=5000
APP_PORT=$BASE_PORT

# Docker-specific config
DOCKER_IMAGE_NAME="$USER_NAME/$REPO_NAME"
DEPLOY_DOCKER_HOST="tcp://ip-172-31-31-76.us-west-1.compute.internal:2375"
CURRENT_DOCKER_HOST=`echo $DOCKER_HOST`

# Extracting the Port number
APP_NUMBER=`echo $DRONE_BUILD_DIR| cut -d'/' -f 8 | cut -d's' -f 2`
if [ ! -z "$APP_NUMBER" -a "$APP_NUMBER" != "" -a "$APP_NUMBER" != " " ]; then
    APP_PORT=`echo $(($BASE_PORT + $APP_NUMBER))`
fi

# export the Docker Host
export DOCKER_HOST=$DEPLOY_DOCKER_HOST

# Get the currently running app instance.
APP_INSTANCE=`docker ps | grep -wo " $REPO_NAME" | cut -d" " -f 2`

# If one instance found, bounce it.
if [ ! -z "$APP_INSTANCE" -a "$APP_INSTANCE" != "" -a "$APP_INSTANCE" != " " ]; then
    echo "Found instance with name: $APP_INSTANCE"

    # Pull New Docker Version ...
    echo "Pulling new version of image: $DOCKER_IMAGE_NAME"
    docker pull $DOCKER_IMAGE_NAME

    # Stopping and starting our app.
    echo "Stopping and Removing instance with name: $APP_INSTANCE"
    docker stop $REPO_NAME; docker rm $REPO_NAME;

    echo "Starting new instance of image: $DOCKER_IMAGE_NAME with name: $APP_INSTANCE"
    docker run -d --name $REPO_NAME -p $APP_PORT:80 $DOCKER_IMAGE_NAME
else
    echo "Instance with name: $REPO_NAME not found."

    # Pull New Docker Version ...
    echo "Pulling new version of image: $DOCKER_IMAGE_NAME"
    docker pull $DOCKER_IMAGE_NAME

    echo "Starting new instance of image: $DOCKER_IMAGE_NAME with name: $REPO_NAME"
    docker run -d --name $REPO_NAME -p $APP_PORT:80 $DOCKER_IMAGE_NAME
fi