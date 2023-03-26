 #!/bin/bash

 filename=$(date '+datadump_%d_%m_%Y.json')
 docker-compose exec app python manage.py dumpdata > $filename