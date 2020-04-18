#!/bin/bash
set -e
ALLOWED_HOSTS=$(echo "$ALLOWED_HOSTS" | sed -r 's/,/ /g')
cp /etc/nginx/nginx_template.conf /etc/nginx/nginx.conf
sed -i "s/ALLOWED_HOSTS/${ALLOWED_HOSTS}/" /etc/nginx/nginx.conf
nginx -g 'daemon off;'