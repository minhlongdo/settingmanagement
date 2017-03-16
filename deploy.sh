#!/bin/sh

$PROD=True
python manage.py makemigrations
python manage.py migrate
docker login -u=$DOCKER_USERNAME -p=$DOCKER_PASSWORD $DOCKER_URL
docker build -t $DOCKER_URL/settingmanage:$APP_MAJOR_VERSION.$APP_MINOR_VERSION.$TRAVIS_BUILD_NUMBER .
docker push $DOCKER_URL/settingmanage:$APP_MAJOR_VERSION.$APP_MINOR_VERSION.$TRAVIS_BUILD_NUMBER