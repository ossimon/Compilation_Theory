import ply.lex as lex


class Lexer:
    def __init__(self):
        self.lexer = lex.lex()
        self.text = ""
        self.tokens = (
            'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
            'SMALLER', 'LARGER', 'SMALLEREQ', 'LARGEREQ', 'NOTEQ', 'EQ',
            'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
            'ADD', 'SUB', 'MUL', 'DIV',
            '(', ')', '[', ']', '{', '}',
            ':',
            'TRANSPOSE',
            ';', ',',
            'IF', 'ELSE', 'FOR', 'WHILE',
            'BREAK', 'CONTINUE', 'RETURN',
            'EYE', 'ZEROS', 'ONCE',
            'PRINT',
            'ID',
            'FLOAT',
            'INT',
            'STRING'
        )
        t_DOTADD = r'.+'
        t_DOTSUB = r'.-'
        t_DOTMUL = r'.*'
        t_DOTDIV = r'./'
        t_SMALLER = r'<'
        t_LARGER = r'>'
        t_SMALLEREQ = r'<='
        t_LARGEREQ = r'>='
        t_NOTEQ = r'!='
        t_EQ = r'=='
        t_ASSIGN = r'='
        t_ADDASSIGN = r'+='
        t_SUBASSIGN = r'-='
        t_MULASSIGN = r'*='
        t_DIVASSIGN = r'/='
        t_ADD = r'+'
        t_SUB = r'-'
        t_MUL = r'*'
        t_DIV = r'/'
        t_( = r'('
        )', '[', ']', '{', '}',
        ':',
        'TRANSPOSE',





    def input(self, text):
        self.text = text
