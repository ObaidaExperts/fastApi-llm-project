"""
Gunicorn configuration for production deployment.
"""
import multiprocessing
import os

# Server socket
bind = os.getenv("GUNICORN_BIND", "127.0.0.1:8000")
backlog = int(os.getenv("GUNICORN_BACKLOG", "2048"))

# Worker processes
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", "1000"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))

# Logging
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")  # stdout
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-")  # stderr
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" '
    '%(D)s %(p)s'
)

# Process naming
proc_name = "fastapi-llm-service"

# Server mechanics
daemon = False
pidfile = os.getenv("GUNICORN_PIDFILE", "/tmp/gunicorn.pid")
umask = 0o007
user = os.getenv("GUNICORN_USER", None)
group = os.getenv("GUNICORN_GROUP", None)
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Performance tuning
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))
preload_app = os.getenv("GUNICORN_PRELOAD_APP", "True").lower() == "true"

# Security
limit_request_line = int(os.getenv("GUNICORN_LIMIT_REQUEST_LINE", "4094"))
limit_request_fields = int(os.getenv("GUNICORN_LIMIT_REQUEST_FIELDS", "100"))
limit_request_field_size = int(os.getenv("GUNICORN_LIMIT_REQUEST_FIELD_SIZE", "8190"))

# Graceful timeout for worker restart
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))

# StatsD (optional, for monitoring)
# statsd_host = "127.0.0.1:8125"
# statsd_prefix = "gunicorn"

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")


def on_exit(server):
    """Called just before exiting Gunicorn."""
    server.log.info("Shutting down: Master")


def worker_int(worker):
    """Called when a worker receives INT or QUIT signal."""
    worker.log.info("worker received INT or QUIT signal")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forking new master process")


def worker_abort(worker):
    """Called when a worker times out."""
    worker.log.info("worker timeout")
