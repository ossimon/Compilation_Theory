import ply.lex as lex

tokens = (
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
    'SMALLER', 'LARGER', 'SMALLEREQ', 'LARGEREQ', 'NOTEQ', 'EQ',
    'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
    'ADD', 'SUB', 'MUL', 'DIV',
    'LPARENT', 'RPARENT', 'LSQBRACK', 'RSQBRACK', 'LCURLBRACK', 'RCURLBRACK',
    'COLON',
    'TRANSPOSE',
    'SEMICOLON', 'COMMA',
    'IF', 'ELSE', 'FOR', 'WHILE',
    'BREAK', 'CONTINUE', 'RETURN',
    'EYE', 'ZEROS', 'ONES',
    'PRINT',
    'ID',
    'FLOAT',
    'INT',
    'STRING'
)
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_SMALLER = r'<'
t_LARGER = r'>'
t_SMALLEREQ = r'<='
t_LARGEREQ = r'>='
t_NOTEQ = r'!='
t_EQ = r'=='
t_ASSIGN = r'='
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LSQBRACK = r'\['
t_RSQBRACK = r'\]'
t_LCURLBRACK = r'{'
t_RCURLBRACK = r'}'
t_COLON = r':'
t_TRANSPOSE = r"'"
t_SEMICOLON = r';'
t_COMMA = r','

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'\d+\.\d*|\d*\.\d+'
    t.value = str(t.value)
    return t

def t_STRING(t):
    r'".*"'
    t.value = str(t.value)
    return t

class Lexer:
    def __init__(self):
        self.lexer = lex.lex()
        self.text = ""

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()