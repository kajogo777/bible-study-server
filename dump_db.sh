 #!/bin/bash

 filename=$(date '+datadump_%d_%m_%Y.json')
 docker exec -it bible-study-server_app_1 python manage.py dumpdata > $filename