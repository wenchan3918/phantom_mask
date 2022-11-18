server {
    listen 80;
    listen [::]:80;

    server_name SERVER_NAME;
#    return 301 https://$host$request_uri;

    include /etc/nginx/conf.d/default.locations;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name SERVER_NAME;
    include /etc/nginx/conf.d/SERVER_NAME.ssl;
    include /etc/nginx/conf.d/default.locations;
}
