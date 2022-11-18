

server {
    listen 80;
    listen [::]:80;
    server_name SERVER_NAME;
    location ~ ^/.well-known/ {
        root /etc/nginx/cert/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}


server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name SERVER_NAME;
    include /etc/nginx/conf.d/SERVER_NAME.ssl;
    include /etc/nginx/conf.d/default.locations;
}
