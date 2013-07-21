uwsgi -s /var/lib/uwsgi_sock/sandy_uwsgi.sock --chdir /usr/local/shared/DataAnywhere/occupysandy/ReST -w flask_ReST:app --touch-reload . --daemonize /var/log/uwsgi/sandy_uwsgi.log --chmod-socket 666
