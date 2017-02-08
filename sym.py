world = {}
class Sym:
    tag = 'sym'
    def __init__(self, V):
        self.val = V ; self.nest = [] ; self.attr = {}
        world[self.val] = self
    def __iadd__(self, o): return self.push(o)
    def push(self, o): self.nest.append(o) ; return o
    def __repr__(self): return self.head()
    def head(self): return '<%s:%s> #%s' % (self.tag, self.val, id(self))
    def dump(self, depth=0):
        S = '\n' + '\t' * depth + self.head()
        for i in self.nest: S += i.dump(depth + 1)
        return S

class Env(Sym): tag='env'
class Pack(Sym): tag = 'pack'
class Class(Sym): tag = 'class'
class Op(Sym): tag = 'op'