#!/bin/bash
set -e

# Activate Virtual Environment
if [[ -e venv/bin/activate ]]; then
    source venv/bin/activate
fi

### Create Service and Log files
#sudo mkdir /var/log/$SERVICE_NAME
#sudo touch /var/log/$SERVICE_NAME/errors.log
#sudo touch /var/log/$SERVICE_NAME/access.log

### Changing Ownership
#sudo chown -R $USER:$GROUP /var/log/$SERVICE_NAME

### Write Gunicorn Configuration
sudo dd of=/home/app/g_config.py << EOF
pidfile = 'web.pid'
worker_class = 'gthread'
workers = 5
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 2
proc_name = 'web01'
bind = '0.0.0.0:5000'
backlog = 2048
accesslog = '/var/log/$SERVICE_NAME/access.log'
errorlog = '/var/log/$SERVICE_NAME/errors.log'
user = '$USER'
group = '$GROUP'
raw_env = [
			'FLASK_APP=/home/$USER/$SERVICE_NAME/app.py',
			'FLASK_ENV=$SERVICE_ENVIRONMENT',
			'FLASK_DEBUG=0',
			'AWS_SECRET_NAME=$AWS_SECRET_NAME',
			'AWS_REGION_NAME=$AWS_REGION_NAME',
			'GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY'
	]
EOF

# set owership and permissions
sudo chown -R $USER:$GROUP /home/app/g_config.py

### Create Service
# sudo dd of=/etc/systemd/system/$SERVICE_NAME.service << EOF
# [Unit]
# Description=Gunicorn instance to serve $SERVICE_NAME web project
# After=network.target

# [Service]
# User=$USER
# Group=www-data
# WorkingDirectory=/home/$USER/$SERVICE_NAME
# Environment="PATH=/home/$USER/$SERVICE_NAME/venv/bin"
# ExecStart=/home/$USER/$SERVICE_NAME/venv/bin/gunicorn --log-level debug --config /home/$USER/$SERVICE_NAME/g_config.py --bind unix:$SERVICE_NAME.sock -m 007 wsgi:app

# [Install]
# WantedBy=multi-user.target
# EOF
 
### Setup AWS CLI
#sudo apt install awscli -y

### Setup AWS
# AWS_CONFIG_FILE=~/.aws/config
# AWS_CREDENTIAL_FILE=~/.aws/credentials

# sudo mkdir ~/.aws
# sudo touch $AWS_CONFIG_FILE
# sudo chmod 600 $AWS_CONFIG_FILE
# sudo chown -R $USER:$GROUP $AWS_CONFIG_FILE

# sudo touch $AWS_CREDENTIAL_FILE
# sudo chmod 600 $AWS_CREDENTIAL_FILE
# sudo chown -R $USER:$GROUP $AWS_CREDENTIAL_FILE

### Setup Credential Configuration
sudo dd of=/home/$USER/.aws/config << EOF
[default]
region = $AWS_REGION_NAME
output = $AWS_DEFAULT_OUTPUT
EOF
### Setup AWS Credentials
sudo dd of=/home/$USER/.aws/credentials << EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOF

exec "$@"