from http.server import HTTPServer, BaseHTTPRequestHandler
import gzip
import io

class SimpleHandler(BaseHTTPRequestHandler):
    def debug_headers(self):
        print("\n--- Received Headers ---")
        for key, value in self.headers.items():
            print(f"{key}: {value}")
        print("-----------------------\n")

    def do_OPTIONS(self):
        self.debug_headers()
        self.send_response(200)
        self.send_header('Allow', 'OPTIONS, POST')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_POST(self):
        self.debug_headers()
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # Check if payload is gzip-compressed
        if self.headers.get('Content-Encoding', '').lower() == 'gzip':
            try:
                print("Oh, we got GZIP encoded data")
                post_data = gzip.decompress(post_data)
                encoding_info = " (decompressed from gzip)"
            except Exception as e:
                response = f"Failed to decompress gzip data: {e}\n".encode('utf-8')
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Content-Length', str(len(response)))
                self.end_headers()
                self.wfile.write(response)
                return
        else:
            encoding_info = ""

        # Try to decode as UTF-8, fallback to hex if not text
        try:
            post_text = post_data.decode('utf-8')
            print(f"Received POST data{encoding_info}:\n{post_text}")
            response = f"Received POST data{encoding_info}:\n{post_text}\n".encode('utf-8')
        except UnicodeDecodeError:
            print(f"Received POST binary data{encoding_info} (not UTF-8):\n{post_data.hex()}")
            response = b"Received POST binary data (not UTF-8):\n" + post_data.hex().encode('utf-8') + b"\n"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()