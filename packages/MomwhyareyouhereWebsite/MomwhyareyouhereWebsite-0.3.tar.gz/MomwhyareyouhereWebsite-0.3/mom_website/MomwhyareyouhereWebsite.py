import os
import http.server
import socketserver

class MomwhyareyouhereWebsite:
    def __init__(self, port=8080, root_directory="."):
        self.port = port
        self.root_directory = root_directory

    def start_server(self):
        os.chdir(self.root_directory)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving HTTP on port {self.port}")
            httpd.serve_forever()

    def add_route(self, route, html_content):
        route_file = os.path.join(self.root_directory, route.lstrip("/"))
        os.makedirs(os.path.dirname(route_file), exist_ok=True)
        with open(route_file, "w") as f:
            f.write(html_content)
