from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import hashlib
from jinja2 import Template

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    template = Template(open("index.html").read())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.template.render(hash_result="").encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode("utf-8"))

        input_text = data.get("input_text", [""])[0]
        hash_result = hashlib.sha256(input_text.encode("utf-8")).hexdigest()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.template.render(hash_result=hash_result).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
