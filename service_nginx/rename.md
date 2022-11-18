# enter container
docker exec -it nginx /bin/sh

##必須在remote server端執行下列指令產生相關憑證
certbot certonly \
--register-unsafely-without-email \
--webroot \
--webroot-path=/etc/nginx/cert -d mask.langgo.app --agree-tos

