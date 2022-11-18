

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


