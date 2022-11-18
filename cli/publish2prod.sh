#!/bin/bash

git add .
git commit -m "script deploy"
git push


#login remote host then git pull and restart container
ssh root@phantom_mask_host << EOF
cd /data/phantom_mask/
git pull
ls -al
# bash run.sh prod build -d django

bash run.sh prod restart django
#bash run.sh prod restart db
bash run.sh prod restart nginx
EOF

