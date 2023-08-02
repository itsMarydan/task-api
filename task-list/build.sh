#!/bin/bash
# Stop running the script on an error
set -e

# Set the variables
DOCKER_BUILD="docker build"

usage () {
  echo "Build script for task-list-api"
  echo "Usage: build.sh [-x -t<tagname>]"
  echo "-x Triggers cross platform build to linux/amd64 (for use on arm systems)"
  echo "-t <tag> Sets tag name for image"
  exit 1
}

while getopts "xht:" options; do
  case "${options}" in
    x)
      DOCKER_BUILD="docker buildx build --platform=linux/amd64 --load"
      ;;
    t)
      TAG=$OPTARG
      ;;
    *)
      usage
      ;;
  esac
done

if [[ $TAG = "" ]];then
  TAG=$(git log -1 --format='%cd-%h' --date=format:%Y%m%d)
fi



final () {
  # Build the runtime container
  echo "Building final container"
  ${DOCKER_BUILD} -t itsmarydan/task-list-api:$TAG .
  # Echo command for running
  echo "Push Command: docker push itsmarydan/task-list-api:$TAG"
  echo "Run Command:  docker run -p 8000:8000 --name task-list-api --rm itsmarydan/task-list-api:$TAG"
  echo ""
}

final

