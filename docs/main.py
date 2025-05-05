import json, http.server, socketserver, subprocess
from translator import translate
from centari_lib import Runtime

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        action, code = self.path.strip('/'), data.get('code','')
        pycode = translate(code)
        rt = Runtime(log_enabled=(action in ['run','log','execute']))
        html, log = '', ''
        if action in ['run','execute','log']:
            html, log = rt.execute(pycode, gui=(action=='run'))
        elif action == 'patch':
            code = rt.patch(code); pycode = translate(code)
            log = '[Patched]\n'
        elif action == 'build':
            # write HTML app and spawn new window
            with open('app.html','w') as f:
                f.write(rt.wrap_html(pycode))
            subprocess.Popen(['xdg-open','app.html'])
            log = '[Built]\n'
        elif action == 'variable':
            name = input('Var name:'); val = input('Value:')
            rt.set_var(name, val); log='[Var set]\n'
        elif action == 'package':
            # uses PyInstaller
            with open('temp.py','w') as f: f.write(pycode)
            subprocess.call(['pyinstaller','--onefile','temp.py'])
            log='[Packaged]\n'
        self.send_response(200)
        self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'html':html,'log':log}).encode())

if __name__=='__main__':
    socketserver.TCPServer(("", PORT), Handler).serve_forever()
