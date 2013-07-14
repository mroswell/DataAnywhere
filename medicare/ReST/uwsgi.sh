uwsgi -s /var/lib/uwsgi_sock/weather_uwsgi.sock --chdir /usr/local/shared/DataAnywhere/weather/ReST -w flask_ReST:app --touch-reload . --daemonize /var/log/uwsgi/uwsgi.log --chmod-socket 666
