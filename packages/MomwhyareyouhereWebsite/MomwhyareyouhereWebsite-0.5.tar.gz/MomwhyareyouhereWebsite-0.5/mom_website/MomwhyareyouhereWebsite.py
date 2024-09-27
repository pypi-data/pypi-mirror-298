import http.server
import socketserver
import os

class MomwhyareyouhereWebsite(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.routes = {}  # Example to hold your routes

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in self.server.routes:
            # Handle your route here
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Handled route")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Route not found")

class Server:
    def __init__(self, port):
        self.port = port
        self.server = MomwhyareyouhereWebsite(('localhost', port), RequestHandler)
        self.server_thread = threading.Thread(target=self.run_server)

    def run_server(self):
        print(f"Serving at port {self.port}")
        self.server.serve_forever()

    def start_server(self):
        self.server_thread.start()

    def stop_server(self):
        print("Shutting down the server...")
        self.server.shutdown()  # This will stop the server
        self.server.server_close()  # This will close the server socket
        self.server_thread.join()  # Wait for the thread to finish
        print("Server stopped.")