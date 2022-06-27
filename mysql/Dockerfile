FROM mysql:8.0.27

# execute startup script(s) on init, these are done alphabetically!
ADD scripts /docker-entrypoint-initdb.d

EXPOSE 3306
EXPOSE 33060
