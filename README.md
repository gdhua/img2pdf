服务器运行
gunicorn -w 2 -b 0.0.0.0:4000 index:app