from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import socketserver
import os


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        if self.path in self.routes:
            # Map the path to the appropriate file
            file_path = os.path.join(self.server.root_directory, self.routes[self.path])

            if os.path.exists(file_path):
                # Serve the file
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                # File not found
                self.send_error(404, "File not found")
        else:
            # Path not mapped, return 404
            self.send_error(404, "Path not found")

class MomwhyareyouhereWebsite:
    def __init__(self, port, root_directory):
        self.port = port
        self.root_directory = root_directory
        self.httpd = None

    def add_route(self, path, file_path):
        CustomHTTPRequestHandler.routes[path] = file_path

    def start_server(self):
        handler = CustomHTTPRequestHandler
        handler.routes = CustomHTTPRequestHandler.routes  # Pass routes to the handler
        server_address = ('', self.port)
        handler.server = self  # Attach the handler to the server instance
        self.httpd = HTTPServer(server_address, handler)
        print(f"Starting server on port {self.port}...")
        self.httpd.serve_forever()

    def stop_server(self):
        print("Stopping server...")
        if self.httpd:
            self.httpd.shutdown()