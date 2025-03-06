import multiprocessing

bind = "0.0.0.0:8080"  # Bind to all IPs and port 8080 (Render uses $PORT)
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal worker count
threads = 2  # Each worker will handle 2 threads
timeout = 120  # Time in seconds before killing a worker
loglevel = "info"
accesslog = "-"  # Log access requests to stdout
errorlog = "-"  # Log errors to stdout
