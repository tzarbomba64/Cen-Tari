import http.server, socketserver, os

PORT = 8000
os.chdir(os.path.join(os.getcwd(), 'docs'))
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()