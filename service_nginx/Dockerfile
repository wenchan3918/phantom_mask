FROM nginx:1.17-alpine

WORKDIR /etc/nginx

RUN apk update \
    && apk add --no-cache python3 augeas python3-dev musl-dev libffi-dev py3-pip gcc openssl-dev\
     mosquitto-clients tzdata openrc php7 ca-certificates wget certbot vim  \
    && cd /root/ \
#    && wget https://github.com/certbot/certbot/archive/v0.22.0.tar.gz \
#    && tar -xzf ./v0.22.0.tar.gz \
#    && cd certbot-0.22.0 \
#    && pip install ./ \
#    && cd .. && rm -rf cd certbot-0.22.0 \
    && pip3 install certbot-nginx letsencrypt



RUN ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime


#CMD ["php","/conf.d/_init.php","nginx", "-g", "daemon off;"]
CMD  . /start.sh