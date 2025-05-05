class Runtime:
    def __init__(self, log_enabled=True):
        self.log = '' if log_enabled else None
        self.vars = {}

    def execute(self, pycode:str, gui=True):
        # exec in a sandbox
        local = {'log':self._log}
        if gui:
            html = f"<pre>{pycode}</pre>"
        else:
            html = ''
        try:
            exec(pycode, {}, local)
        except Exception as e:
            self._log(f"Error: {e}\n")
        return html, self.log or ''

    def _log(self, msg):
        if self.log is not None: self.log += str(msg)

    def patch(self, code:str) -> str:
        # dummy: just return code
        return code

    def wrap_html(self, pycode:str):
        return f"<html><body><script>console.log('Running');</script><pre>{pycode}</pre></body></html>"

    def set_var(self, name, val):
        self.vars[name] = val
        self._log(f"{name} = {val}\n")
