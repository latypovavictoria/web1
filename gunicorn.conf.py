import multiprocessing
bind="192.168.181.169:8000"
workers=multiprocessing.cpu_count()*2+1
accesslog='/var/tmp/technopark.gunicorn.log'