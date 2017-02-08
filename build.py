log = open('log.log','w')

import ply.lex  as lex
import ply.yacc as yacc

from sym import *

tokens = [ 'SYM' , 'CLASS' , 'PACK' , 'PERC','DIV','EQ' ]

t_ignore = ' \t\r'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 
def t_ignore_comment(t):
    r'\#.*'
def t_CLASS(t):
    r'class'
    t.value = Class(t.value) ; return t
def t_PACK(t):
    r'pack'
    t.value = Pack(t.value) ; return t
def t_PERC(t):
    r'\%'
    t.value = Op(t.value) ; return t
def t_DIV(t):
    r'\/'
    t.value = Op(t.value) ; return t
def t_EQ(t):
    r'\='
    t.value = Op(t.value) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t

def p_REPL(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print >>log,p[2].dump()
    print >>log,'-'*20
    for i in world: print >>log,world[i]
    print >>log,'='*40
def p_ex(p):
    ' ex : SYM '
    p[0] = p[1]

def p_ex_class(p):
    ' ex : class '
    p[0] = p[1]
def p_class(p):
    ' class : CLASS SYM '
    p[0] = Class(p[2].val)
def p_ex_pack(p):
    ' ex : pack '
    p[0] = p[1]
def p_pack(p):
    ' pack : PACK SYM '
    p[0] = Pack(p[2].val)
    
def p_ex_perc(p):
    ' ex : ex PERC ex '
    p[0] = p[1] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_eq(p):
    ' ex : ex EQ ex '
    p[0] = p[1] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_div(p):
    ' ex : ex DIV ex '
    p[0] = p[1] ; p[0] += p[1] ; p[0] += p[3]

def t_error(t): print 'lexer/error', t
def p_error(p): print 'parse/error', p

lex.lex() 
yacc.yacc(debug=False, write_tables=False).parse(open('main.bI').read())
