import os
import json
from wsgiref.simple_server import make_server


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/health":
        status = "200 OK"
        payload = {"status": "ok"}
    elif path == "/":
        status = "200 OK"
        payload = {
            "app": "HelpDesk Cloud",
            "db_host": os.environ.get("DB_HOST", "non défini"),
            "bucket": os.environ.get("S3_BUCKET", "non défini"),
        }
    else:
        status = "404 Not Found"
        payload = {"error": "Not Found"}

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    start_response(status, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ])
    return [body]

if __name__ == "__main__":
    with make_server("0.0.0.0", 5000, app) as server:
        server.serve_forever()