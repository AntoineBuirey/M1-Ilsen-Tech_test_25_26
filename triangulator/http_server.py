"""HTTP server module for the triangulator application."""

import flask as fk

from .triangulator import get_and_compute

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
        @self.route("/triangulation/<point_set_id>", methods=["GET"])
        def triangulation(point_set_id: str):
            try:
                triangles = get_and_compute(point_set_id)
                return fk.Response(triangles, status=200, mimetype="application/octet-stream")
            except KeyError as e:
                return fk.jsonify({"code": "NOT FOUND", "message": str(e)}), 404
            except ValueError as e:
                return fk.jsonify({"code": "BAD REQUEST", "message": str(e)}), 400
            except ConnectionError as e:
                return fk.jsonify({"code": "SERVICE UNAVAILABLE", "message": str(e)}), 503
            except Exception as e:
                return fk.jsonify({"code": "INTERNAL SERVER ERROR", "message": str(e)}), 500
