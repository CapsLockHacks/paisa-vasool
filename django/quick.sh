#/bin/sh

docker-compose down
git fetch --all
git pull origin master
docker-compose build
docker-compose up
