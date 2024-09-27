from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import time
import socketserver
import os

class MomwhyareyouhereWebsite(HTTPServer):
    def __init__(self, port, root_directory):
        super().__init__(('localhost', port), RequestHandler)
        self.routes = {}
        self.root_directory = root_directory
        self.server_thread = threading.Thread(target=self.serve_forever)

    def add_route(self, route, file_path):
        self.routes[route] = file_path

    def start_server(self):
        print(f"Serving on port {self.server_address[1]}...")
        self.server_thread.start()

    def stop_server(self):
        print("Stopping the server...")
        self.shutdown()  # Shut down the server
        self.server_close()  # Close the server socket
        self.server_thread.join()  # Wait for the thread to finish
        print("Server stopped.")

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html when the root is accessed
        if self.path == '/':
            self.path = '/index.html'  # Change the path to index.html
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