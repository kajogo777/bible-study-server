 #!/bin/bash

if [ -z $1 ];
then
    echo "Missing dump path"
    exit 1
fi

echo "Loading dump $1"
docker-compose exec app python manage.py loaddata -e contenttypes $1