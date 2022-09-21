"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Tasks Class.  Implementation of Celery Tasks
Notifyees: craig@2deviate.com
Category: None
"""
from celery import Celery
import logging


logger = logging.getLogger(__name__)


app = Celery('async',
             broker="redis://localhost",
             include=['async.tasks'])

app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    app.start()

#celery -A async worker -l INFO
