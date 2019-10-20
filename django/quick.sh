#/bin/sh

docker-compose down
git fetch --all
git pull origin master
docker-compose build
docker-compose run --rm web python manage.py migrate # Run new migrations
docker-compose up -d
