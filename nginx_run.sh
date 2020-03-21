#!/bin/bash
set -e
ALLOWED_HOSTS=$(echo "$ALLOWED_HOSTS" | sed -r 's/,/ /g')
sed -i "s/ALLOWED_HOSTS/${ALLOWED_HOSTS}/" /etc/nginx/nginx.conf
cat /etc/nginx/nginx.conf
nginx -g 'daemon off;'