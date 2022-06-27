# Pangea Exchange Web Server
Simple Flask Web Server which allows User(s) to search for PSTN decommissions.

## Description
The web server uses several API's to bind data together and determine which exchanges (Openreach PSTN) are being decommissioned.

## Getting Started

### Dependencies
* Docker, Alpine Images
* RDS MySql Database Image
* Python Flask Application with package dependencies
    * requirements.txt - file contains package dependencies
    * etl.py - script to load the data manually
    * notifier.py - script to schedule the processing of uploads and queries
* AWS Secrets (or other) for boto configuration (Discontinued)

## Installing Web Server on AWS (Optional)

### Setup AWS EC2 Web Server (Ubuntu)
In this example a t2.micro aws EC2 instance is setup via the EC2 dashboard.  See references below for links.

### Docker Requirements
    Access to Docker Repository e.g. Docker Hub, or equivalent
    Access to Docker CLI (Windows, Mac or Unix)

### Dowloading and installing images locally
    Install Docker CLI
    Docker login <<Provide Repo Credentials>>
    
    docker pull << repo/tag >> e.g. docker pull 2deviate/pangea-server:v1.0

### Building Docker Images
    docker compose --env-file  << environment file >> up -d
    docker compose --env-file ./config/.env.dev up -d

### Publishing Docker Images
    docker compose push

### Create SystemCtl Service
    cd /etc/systemd/system/
    vi pangea.service

### Installing AWSCLI (Optional)
    sudo apt install awscli
    aws configure

### Enter Key, Secret key and region (output of aws cli listing)
    profile                <not set>             None    None
    access_key     ****************HBVX shared-credentials-file
    secret_key     ****************gHQz shared-credentials-file
    region         eu-west-2      config-file    ~/.aws/config

### Setup environment variable (*DEBUG PURPOSES ONLY)
    All environment variables are provided in a single file, .env.<<environment>> e.g. .env.dev

    LOGFILENAME                     - log file name for application (web)
    LOGLEVEL                        - logging level 
    FLASK_APP                       - Flask (www) Application Name
    FLASK_ENV                       - Flask Environment
    FLASK_PORT                      - Flask Port
    FLASK_HOST                      - Flask Host
    FLASK_DEBUG                     - Flask Debug
    FLASK_APP_TEMPLATE_NAME         - Flask App template used for
    FLASK_APP_UPLOAD_FOLDER         - Flask file upload folder path
    FLASK_APP_DOWNLOAD_FOLDER       - Flask file download folder path
    FLASK_FILE_UPLOAD_MAX_LENGTH    - Maximum length (bytes) of file upload
    MYSQL_USER                      - MySql user name
    MYSQL_PASSWORD                  - MySql user password
    MYSQL_HOST                      - MySql server host address
    MYSQL_PORT                      - MySql server port no.
    MYSQL_DATABASE                  - MySql database name
    DOCKER_DB_NAME                  - Docker default database name (service)
    DOCKER_SERVER_NAME              - Docker default server name (service)
    DOCKER_PROXY_NAME               - Docker default proxy name (service)
    GOOGLE_MAPS_API_KEY             - Google maps api key
    SMTP_USER                       - SMTP mail user name
    SMTP_PASSWORD                   - SMTP mail password
    SMTP_HOST                       - SMTP mail host address
    SMTP_PORT                       - SMTP mail server port no.
    EMAIL_FROM_ADDRESS              - Email from address
    EMAIL_CC_ADDRESSES              - Email cc address(es)
    EMAIL_ATTACHMENT                - Email attachement
    EMAIL_SUBJECT                   - Email subject
    EMAIL_TEMPLATE_SCHEMA           - Email template Schema (table column headers)
    PROXY_SERVER                    - Proxy server address e.g. 8000:server

## Setting up Scheduled Jobs
Cron is setup as part of the server image.  The cron is crond (daemon) and is run as root on startup.  The scheduling
allows for various files dropped into /etc

notification.sh -> invokes notification.py (every 15min)
etl.sh -> invokes etl.py (once a day)

# do daily/weekly/monthly maintenance
# min   hour    day     month   weekday command
*/15    *       *       *       *       run-parts /etc/periodic/15min       /notification
0       *       *       *       *       run-parts /etc/periodic/hourly
0       2       *       *       *       run-parts /etc/periodic/daily       /etl
0       3       *       *       6       run-parts /etc/periodic/weekly
0       5       1       *       *       run-parts /etc/periodic/monthly

## Authors

## Contributors names and contact info
    Craig Petersen[craig@2deviate.com)

## Version History
    0.2
        * Initial Release
        * Added File Upload

## License
This project is licensed under 2DEVIATE LTD License agreement.

## References
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04

https://www.docker.com/?utm_source=google&utm_medium=cpc&utm_campaign=search_emea_brand&utm_term=docker_exact&gclid=CjwKCAjwquWVBhBrEiwAt1KmwiyOmuWjcwg0aBw23HFzaIzdqxMYBKMG4y0RmBYmPz7qz09rIv7qChoC_GcQAvD_BwE

https://www.alpinelinux.org/




