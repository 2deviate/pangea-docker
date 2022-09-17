FROM 2deviate/alpine-pandas

USER root

ARG GOOGLE_MAPS_API_KEY
# environment variables
ENV GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}

# permissions and ubuntu (nonroot) user for tightened security
RUN addgroup -S ubuntu && \
    adduser -D ubuntu -G ubuntu -h /home/ubuntu && \
    echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu

# var logs
RUN mkdir /home/app/ && chown -R ubuntu:ubuntu /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R ubuntu:ubuntu /var/log/flask-app

# aws configuration
RUN mkdir /home/ubuntu/.aws && chown -R ubuntu:ubuntu /home/ubuntu/.aws
RUN mkdir -p /home/ubuntu/.aws && touch /home/ubuntu/.aws/config && touch /home/ubuntu/.aws/credentials
RUN chown -R ubuntu:ubuntu /home/ubuntu/.aws

COPY etl.sh /etc/periodic/daily/etl
COPY notifier.sh /etc/periodic/15min/notifier
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /etc/periodic/daily/etl
RUN chmod +x /etc/periodic/15min/notifier
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /home/app

USER ubuntu

# copy all the files to the container
COPY --chown=ubuntu:ubuntu . .

# python setup
RUN python -m venv --system-site-packages /home/app/venv
ENV PATH="/home/app/venv/bin:$PATH"

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN chmod +x etl.sh
RUN chmod +x notifier.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]