 #!/bin/bash

if [ -z $1 ];
then
    echo "Missing dump path"
    exit 1
fi

echo "Loading dump $1"
docker exec -it bible-study-server_app_1 python manage.py loaddata $1