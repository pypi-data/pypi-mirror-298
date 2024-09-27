import http.server
import socketserver
import os

class MomwhyareyouhereWebsite:
    def __init__(self, port=8080, root_directory="website"):
        self.port = port
        self.root_directory = root_directory
        self.routes = {}

    def add_route(self, route, content):
        """Add a route to the server. Content can be an HTML string or a file path."""
        if os.path.isfile(content):
            with open(content, 'r') as file:
                content = file.read()
        self.routes[route] = content

    def start_server(self):
        """Start the HTTP server."""
        handler = self.create_handler()
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving at port {self.port}")
            httpd.serve_forever()

    def create_handler(self):
        """Create a request handler that serves the routes."""
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path in self.server.routes:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(self.server.routes[self.path].encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"404 Not Found")
        
        return CustomHandler
