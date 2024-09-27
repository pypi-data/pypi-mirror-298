import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Any

import typer
from typing_extensions import override

from cli import settings

from . import auth_tokens
from .rest_helper import RestHelper as Rest

HELP = """
Manage how you authenticate with our cloud platform
"""

httpd: HTTPServer

app = typer.Typer(help=HELP)
app.add_typer(auth_tokens.app, name="tokens", help="Manage users personal access tokens")


class S(BaseHTTPRequestHandler):
    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    @override
    def log_message(self, format: Any, *args: Any) -> None:  # pylint: disable=W0622,
        return

    # Please do not change this into lowercase!
    @override
    # type: ignore
    def do_GET(self):  # pylint: disable=invalid-name,
        self._set_response()
        self.wfile.write("Successfully setup CLI, return to your terminal to continue".encode("utf-8"))
        path = self.path
        time.sleep(1)
        httpd.server_close()

        killerthread = Thread(target=httpd.shutdown)
        killerthread.start()

        settings.write_secret_token(path[1:])
        print("Successfully logged on, you are ready to go with cli")


def start_local_webserver(server_class: type = HTTPServer, handler_class: type = S, port: int = 0) -> None:
    server_address = ("", port)
    global httpd  # pylint: disable=W0603
    httpd = server_class(server_address, handler_class)


#
# CLI commands go here
#


@app.command(name="login")
def login() -> None:
    """
    Login to the cli using browser

    This will be used as the current access token in all subsequent requests. This would
    be the same as activating a personal access key or service-account access key.
    """
    start_local_webserver()
    webbrowser.open(
        f"{Rest.get_base_url()}/login?redirectUrl=http://localhost:{httpd.server_address[1]}",
        new=1,
        autoraise=True,
    )

    httpd.serve_forever()


@app.command()
def whoami() -> None:
    """
    Validates authentication and fetches your user information
    """
    Rest.handle_get("/api/whoami")


@app.command()
def print_access_token() -> None:
    """
    Print current active access token
    """
    print(settings.read_secret_token())


@app.command(help="Clear access token")
def logout() -> None:
    settings.clear_secret_token()
    print("Access token removed")
