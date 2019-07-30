import multiprocessing
import os

host = os.getenv('HOST', '0.0.0.0')
port = str(os.getenv('PORT', 3000))
bind = ':'.join([host, port])
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2
