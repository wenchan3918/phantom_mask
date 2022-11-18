echo "running nginx start.sh"
#locale -a
server_name_list=$(echo $SERVER_NAME_LIST | tr "," "\n")
rm -rf /etc/nginx/conf.d/*.conf
rm -rf /etc/nginx/conf.d/*.ssl

for server_name in $server_name_list; do
  server_name=$(echo $server_name | sed -e 's/^[[:space:]]*//')
#  echo $server_name

  #建立conf
  if [ "$MODE" = "prod" ]; then
    echo 'prod...';
    cat /etc/nginx/conf.d/conf-prod.tpl >>/etc/nginx/conf.d/${server_name}.conf
    sed "s/SERVER_NAME/$server_name/g" /etc/nginx/conf.d/conf-prod.tpl > /etc/nginx/conf.d/${server_name}.conf
  else
    echo 'dev...';
    cat /etc/nginx/conf.d/conf-dev.tpl >>/etc/nginx/conf.d/${server_name}.conf
    sed "s/SERVER_NAME/$server_name/g" /etc/nginx/conf.d/conf-dev.tpl > /etc/nginx/conf.d/${server_name}.conf
  fi


  #建立ssl憑證
  echo -en "ssl_certificate /etc/letsencrypt/live/${server_name}/fullchain.pem;\n" \
    "ssl_certificate_key /etc/letsencrypt/live/${server_name}/privkey.pem;" >>/etc/nginx/conf.d/${server_name}.ssl
  done

#因為cron凌晨一點更新ssl憑證，最多隔12小時會reload(凌晨5點)
nginx -g "daemon off;" & trap exit TERM; while :; do certbot renew ; nginx -s reload; echo nginx_reload;sleep 12h & wait ${!}; done
