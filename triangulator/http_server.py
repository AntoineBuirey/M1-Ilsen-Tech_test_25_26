"""HTTP server module for the triangulator application."""

import flask as fk


class HTTPServer(fk.Flask):
    """HTTP server for the triangulator application.

    Args:
        name (str): The name of the Flask application.

    """

    def __init__(self, name: str):
        """Initialize the HTTP server."""
        super().__init__(name)
        self.configure_routes()

    def configure_routes(self):
        """Configure the routes for the HTTP server."""
        pass
