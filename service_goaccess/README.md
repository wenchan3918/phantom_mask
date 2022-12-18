#Configuration

## Add Service to docker-compose.yml
Path in docker-compose.yml
```shell
  goaccess:
    image: "gregyankovoy/goaccess"
    container_name: goaccess
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "1g"
    environment:
      TZ: "Asia/Taipei"
    env_file: .env
    volumes:
      - ./log:/opt/log
      - ./service_goaccess:/config/
    networks:
      phantom_mask_net:

```


## Add port to docker-compose-{dev,prod}.yml
Path in docker-compose-{dev,prod}.yml
```shell
    goaccess:
    expose:
      - 7889
```

# Modify log-file path in service_goaccess/goaccess.conf
add to line 330:
```shell
# Specify the path to the input log file. If set, it will take
# priority over -f from the command line.
#
log-file /opt/log/nginx-access.log
```


## Add upstream to conf-{dev,prod}.tpl
Path in service_nginx/conf.d/conf-{dev,prod}.tpl

```shell
upstream ws_goaccess {
    server goaccess:7889;
}
```


## Add location to default.locations
Path in service_nginx/conf.d/default.locations

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
