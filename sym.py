world = {}
class Sym:
    tag = 'sym'
    def __init__(self, V):
        if V in world: world[V].ref += 1
        self.ref = 0 ; self.doc = ''
        self.val = V ; self.nest = [] ; self.attr = {}
        world[V] = self
    def __iadd__(self, o): return self.push(o)
    def push(self, o): self.nest.append(o) ; return self
    def __mod__(self, o):
        if o.tag in ['var']: self.attr[o.val] = o.nest[0] 
        else: self.attr[o.val] = o
        return self
    def __repr__(self): return self.head()
#     def __str__(self): return str(self.val)
    def head(self):
        return '<%s:%s> @%s #%s %s' % (
            self.tag, self.val, id(self), self.ref, self.doc)
    def dump(self, depth=0):
        S = '\n' + '\t' * depth + self.head()
        for i in self.attr:
            S += '\n' + '\t' * (depth + 1) + i + ' ='
            S += self.attr[i].dump(depth + 2)
        for i in self.nest: S += i.dump(depth + 1)
        return S
    def __div__(self,o): raise BaseException('%s / %s'%(self,o))

class Env(Sym): tag='env'
glob = Env('global')

class Str(Sym):
    tag = 'str'
    def head(self):
        return "'%s' @%s #%s %s" % (self.val, id(self), self.ref, self.doc)

class Num(Sym):
    tag = 'num'
    def __init__(self, V): Sym.__init__(self, float(V))
    def head(self):
        return "%s @%s #%s %s" % (self.val, id(self), self.ref, self.doc)
    def __div__(self,o):
        if o.tag != 'num': Sym.__div__(self,o)
        else: return Num(self.val / o.val) 

class Var(Sym):
    tag = 'var'
    def __init__(self,E,A,B):
        Sym.__init__(self, A.val) ; self.push(B) ; self.doc = A.doc
        E.push(self)
    
class Op(Sym): tag = 'op'

class Pack(Env):
    tag = 'pack'
    def __init__(self,V): Sym.__init__(self, V) ; glob.push(self)
    def __div__(self,o):
        if o.tag == 'class': return self.push(o)
        else: return Sym.__div__(self, o)

class Class(Sym): tag = 'class'
