#!/bin/bash
envsubst '$PROXY_SERVER' < /tmp/default.conf > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'