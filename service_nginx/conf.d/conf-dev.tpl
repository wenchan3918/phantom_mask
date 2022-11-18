server {
    listen 80;
    listen [::]:80;
    server_name SERVER_NAME;
#    return 301 https://$host$request_uri;
    include /etc/nginx/conf.d/default.locations;
}

