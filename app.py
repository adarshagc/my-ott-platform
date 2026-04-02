import http.server
import socketserver
import os

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. If it's the home page
        if self.path == '/':
            self.path = '/index.html'
            return super().do_GET()
        
        # 2. Check if the file is in the main folder
        if os.path.exists(self.path.lstrip('/')):
            return super().do_GET()
        
        # 3. FIX: Look specifically inside assets/videos
        # We manually build the path to the movie
        clean_path = self.path.lstrip('/')
        # We need to unquote the URL (e.g., %20 becomes a space)
        from urllib.parse import unquote
        video_file = unquote(clean_path)
        
        full_video_path = os.path.join(BASE_DIR, 'assets', 'videos', video_file)
        
        if os.path.exists(full_video_path):
            # Tell Python: "Ignore the URL path, use THIS actual file path"
            self.path = f"/assets/videos/{video_file}"
            return super().do_GET()
            
        return super().do_GET()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server started at http://192.168.29.219:{PORT}")
    httpd.serve_forever()