import re

def translate(code:str) -> str:
    # very naive mix of HTML/Java/C# style → Python
    code = code.replace('var ', '')  # strip var
    code = re.sub(r'//(.+)', r'#\1', code)  # comments
    # TODO: add real parser for function(), class, etc.
    return code
