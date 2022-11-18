#!/bin/bash

:||{
指令範例:
bash run.sh local up db

bash run.sh dev up -d
bash run.sh dev restart

bash run.sh prod up -d
bash run.sh prod restart
}

current_path=$(cd "$(dirname "$0")"; pwd -P)
echo $current_path

mode='local'
dc_args=''

args=("$@")
for ((i=0; i < $#; i++))
{
    if [[ $i == 0 ]];then
      mode=${args[$i]};
    else
      dc_args+="${args[$i]} "
    fi;
}
echo $dc_args;

if [ $mode == 'local' ];then
  docker-compose \
  -f "${current_path}/docker-compose-${mode}.yml" \
  $dc_args

elif [ $mode == 'dev' ];then
    docker-compose \
    -f "${current_path}/docker-compose.yml" \
    -f "${current_path}/docker-compose-${mode}.yml" \
    $dc_args

elif [ $mode == 'prod' ];then
    docker-compose \
    -f "${current_path}/docker-compose.yml" \
    -f "${current_path}/docker-compose-${mode}.yml" \
    $dc_args

fi