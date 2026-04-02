import http.server
import socketserver
import os
import json
from urllib.parse import unquote

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # NEW: A secret "API" route to get the list of movies
        if self.path == '/api/movies':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            video_dir = os.path.join(BASE_DIR, 'assets', 'videos')
            # Get only .mp4 files for now
            movies = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
            self.wfile.write(json.dumps(movies).encode())
            return

        if self.path == '/':
            self.path = '/index.html'
        
        # Standard video handling
        clean_path = unquote(self.path.lstrip('/'))
        if clean_path.endswith('.mp4'):
            video_path = os.path.join(BASE_DIR, 'assets', 'videos', clean_path)
            if os.path.exists(video_path):
                self.path = f"/assets/videos/{clean_path}"
        
        return super().do_GET()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

with ThreadingHTTPServer(("", PORT), MyHandler) as httpd:
    print(f"OTT System Live: http://192.168.29.219:{PORT}")
    httpd.serve_forever()