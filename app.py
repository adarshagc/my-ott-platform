import http.server
import socketserver
import os

PORT = 8000

# This line is the magic fix. It finds the folder where app.py is saved.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. If asking for home page, force it to show index.html
        if self.path == '/':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # 2. Check if the file exists in the main folder (like index.html)
        if os.path.exists(self.path.lstrip('/')):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # 3. If not found, look inside assets/videos
        # This maps "500 Days of Summer.mp4" to "assets/videos/500 Days of Summer.mp4"
        video_path = os.path.join('assets', 'videos', self.path.lstrip('/'))
        if os.path.exists(video_path):
            self.path = video_path
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server started at http://192.168.29.219:{PORT}")
    httpd.serve_forever()