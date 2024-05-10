import ply.lex as lex
from flask import Flask, request, render_template

tokens = (
    'FOR', 'IF', 'DO', 'WHILE', 'ELSE', 'LPAREN', 'RPAREN', 'NEWLINE'
)

t_FOR = r'for'
t_IF = r'if'
t_DO = r'do'
t_WHILE = r'while'
t_ELSE = r'else'
t_LPAREN = r'\('
t_RPAREN = r'\)'
NEWLINE = r'\n'

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Manejar los saltos de línea
def NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = ''
        file = request.files.get('file')
        if file and file.filename.endswith('.txt'):
            code = file.read().decode('utf-8')
        else:
            code = request.form.get('code', '')

        lexer.input(code)
        token_list = []
        current_line = 1
        for token in lexer:
            token_list.append({
                'type': token.type,
                'value': token.value,
                'line': current_line
            })
            current_line += 1
        return render_template('index.html', tokens=token_list)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
