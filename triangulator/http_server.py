import flask as fk

class HTTPServer(fk.Flask):
    def __init__(self, name: str):
        super().__init__(name)
        self.configure_routes()

    def configure_routes(self):
        pass
