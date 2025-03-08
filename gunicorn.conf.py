import multiprocessing

bind = "0.0.0.0:8000"
workers = workers = 2  # Adjust based on Render memory limits
worker_class = "uvicorn.workers.UvicornWorker"
threads = 2  # Each worker will handle 2 threads
timeout = 300  # Time in seconds before killing a worker
loglevel = "info"
accesslog = "-"  # Log access requests to stdout
errorlog = "-"  # Log errors to stdout
