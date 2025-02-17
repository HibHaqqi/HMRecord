# gunicorn_config.py

workers = 3
bind = "0.0.0.0:8000"
timeout = 120
accesslog = "/home/hibhaqqi/gunicorn/logs/access.log"
errorlog = "/home/hibhaqqi/gunicorn/logs/error.log"
loglevel = "info"
daemon = False
user = "hibhaqqi"
group = "hibhaqqi"
pidfile = "/home/hibhaqqi/gunicorn/pid/gunicorn.pid"
