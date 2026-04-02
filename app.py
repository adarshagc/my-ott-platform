import http.server
import socketserver
import os

# This tells Python to look inside your assets/videos folder
PORT = 8000
DIRECTORY = "assets/videos"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"OTT Server started at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()