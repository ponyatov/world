log = open('log.log','w')
 
import ply.lex  as lex
import ply.yacc as yacc
 
from sym import *
 
tokens = [ 'SYM' , 'NUM' , 'STR' , 'DOC' ,
          'LP' , 'RP' ,
          'EQ' , 'DIV' , 'PERC' ,
          'CLASS' , 'PACK' ]

states = (('str','exclusive'),('doc','exclusive'))

t_doc_ignore = ''
def t_DOC(t):
    r'\"'
    t.lexer.lexstring = ''
    t.lexer.begin('doc')
def t_doc_DOC(t):
    r'\"'
    t.lexer.begin('INITIAL')
    t.value = Str(t.lexer.lexstring) ; return t
def t_doc_char(t):
    r'.'
    t.lexer.lexstring += t.value

t_str_ignore = ''
def t_STR(t):
    r'\''
    t.lexer.lexstring=''
    t.lexer.begin('str')
def t_str_STR(t):
    r'\''
    t.lexer.begin('INITIAL')
    t.value = Str(t.lexer.lexstring) ; return t
def t_str_char(t):
    r'.'
    t.lexer.lexstring += t.value
 
t_ignore = ' \t\r'
def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 
def t_ignore_comment(t):
    r'\#.*'
def t_CLASS(t):
    r'class'
    t.value = Sym(t.value) ; return t
def t_PACK(t):
    r'pack'
    t.value = Sym(t.value) ; return t
    
def t_LP(t):
    r'\('
    t.value = Op(t.value) ; return t
def t_RP(t):
    r'\)'
    t.value = Op(t.value) ; return t
    
def t_PERC(t):
    r'\%'
    t.value = Op(t.value) ; return t
def t_DIV(t):
    r'\/'
    t.value = Op(t.value) ; return t
def t_EQ(t):
    r'\='
    t.value = Op(t.value) ; return t
def t_NUM(t):
    r'[0-9]+(\.[0-9]*)?([eE][\+\-]?[0-9]+)?'
    t.value = Num(t.value) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t
    
precedence = (
    ('left','PERC'),
    ('right','EQ'),
    ('nonassoc','DOC'),
    )
 
def p_REPL(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print >>log,p[2].dump()
    print >>log,'-'*20
    print >>log,glob.dump()
    print >>log,'-'*20
    for i in world: print >>log,i,world[i].head()
    print >>log,'='*40
 
def p_ex(p):
    ' ex : scalar '
    p[0] = p[1]
def p_scalar(p):
    ''' scalar : SYM
                | NUM
                | STR '''
    p[0] = p[1]
 
def p_ex_pack(p):
    ' ex : pack '
    p[0] = p[1]
def p_pack(p):
    ' pack : PACK SYM '
    p[0] = Pack(p[2].val)
def p_ex_class(p):
    ' ex : class '
    p[0] = p[1]
def p_class(p):
    ' class : CLASS SYM '
    p[0] = Class(p[2].val)

def p_ex_colons(p):
    ' ex : LP ex RP '
    p[0] = p[2]
def p_ex_perc(p):
    ' ex : ex PERC ex '
    p[0] = p[1] % p[3]
def p_ex_div(p):
    ' ex : ex DIV ex '
    p[0] = p[1] / p[3]
def p_ex_eq(p):
    ' ex : ex EQ ex '
    p[0] = Var(glob,p[1], p[3])

def p_ex_DOC(p):
    ' ex : ex DOC '
    p[0] = p[1] ; p[0].doc = p[2].val    
 
def t_ANY_error(t): print 'lexer/error', t
def p_error(p): print 'parse/error', p
 
lex.lex() 
yacc.yacc(debug=False, write_tables=False).parse(open('main.bI').read())
