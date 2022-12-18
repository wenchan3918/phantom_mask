#Nginx configuration

## Add upstream to conf-dev.tpl/conf-prod.tpl
path in service_nginx/conf.d/conf-dev.tpl and service_nginx/conf.d/conf-prod.tpl

```shell
upstream ws_goaccess {
    server goaccess:7889;
}
```


## Add location to default.locations
path in service_nginx/conf.d/default.locations

```shell
location /goaccess {
    set $upstream_goaccess ws_goaccess;
    proxy_pass http://$upstream_goaccess/;

    proxy_connect_timeout 1d;
    proxy_send_timeout 1d;
    proxy_read_timeout 1d;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
}

```


# TODO
- [ ] Only admin can view
