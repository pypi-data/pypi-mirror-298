from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import time
import socketserver
import os


class MomwhyareyouhereWebsite:
    def __init__(self, port, root_directory):
        self.port = port
        self.root_directory = root_directory
        self.httpd = None

    def add_route(self, path, file_path):
        handler = SimpleHTTPRequestHandler
        handler.directory = self.root_directory
        handler.extensions_map['.html'] = 'text/html'
        
        self.httpd = HTTPServer(('', self.port), handler)

    def start_server(self):
        print(f"Starting server on port {self.port}...")
        if self.httpd:
            self.httpd.serve_forever()

    def stop_server(self):
        print("Stopping server...")
        if self.httpd:
            self.httpd.shutdown()

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html when the root is accessed
        if self.path == '/':
            self.path = '/index.html'  # Serve index.html for root access
        # Serve the requested file if it exists in the routes
        if self.path in self.server.routes:
            self.send_response(200)
            self.end_headers()
            with open(self.server.routes[self.path], 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")