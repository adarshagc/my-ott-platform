import http.server
import socketserver
import os
from urllib.parse import unquote

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # This tells the browser it's okay to stream this data
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return super().do_GET()
        
        # Decode the URL (fixes spaces and special characters)
        clean_path = unquote(self.path.lstrip('/'))
        
        # Check if it's a video file
        if clean_path.endswith(('.mp4', '.mkv', '.webm')):
            video_path = os.path.join(BASE_DIR, 'assets', 'videos', clean_path)
            if os.path.exists(video_path):
                self.path = f"/assets/videos/{clean_path}"
        
        return super().do_GET()

# Use a faster threading server to handle multiple "chunks" of video at once
class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

with ThreadingHTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Streaming Server active at http://192.168.29.219:{PORT}")
    httpd.serve_forever()