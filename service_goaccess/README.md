#Nginx configuration

## Add upstream to conf-dev.tpl/conf-prod.tpl

```shell
upstream ws_goaccess {
    server goaccess:7889;
}
```