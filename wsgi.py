from pkg import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = create_app()

def not_found(environ, start_response):
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]

application = DispatcherMiddleware(not_found, {
    "/talentbridge": app
}) = "/talentbridge"