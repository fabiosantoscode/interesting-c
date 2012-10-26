




class TraversalMixin(object):
    def get_parent(self):
        if not self.parent:
            raise Exception('At root node')
        return self.parent
    
    def get_silblings(self):
        same_level = self.get_all_in_level()
        same_level.remove(self)
        return same_level
    
    def get_all_in_level(self):
        return list(self.parent.children)
    
    def get_next(self):
        same_lvl = self.get_all_in_level()
        ind = same_lvl.index(self)
        if ind == len(same_lvl) - 1:
            raise IndexError
        return same_lvl[ind+1] 
    
    def get_previous(self):
        same_lvl = self.get_all_in_level()
        ind = same_lvl.index(self)
        if ind == 0:
            raise IndexError
        return same_lvl[ind-1]
    
    def ancestors(self):
        current = self.parent
        while current:
            yield current
            current = current.parent
    
    def get_ancestor(self, condition):
        for ancestor in self.ancestors():
            if condition(ancestor):
                return ancestor
        raise Exception('Ancestor not found.')



class LangTraversalMixin(object):
    def get_namespace(self):
        if getattr(self, 'namespace', None):
            return self.namespace
        else:
            has_ns = lambda node: getattr(node, 'namespace', False)
            return self.get_ancestor(condition=has_ns).namespace



class SyntaxTreeNode(TraversalMixin, LangTraversalMixin, object):
    def __init__(self, children=[], leaf=None):
        self.parent = None
        self.children = children
        self.integrate_children()
        self.leaf = leaf
    
    def integrate_children(self):
        for child in self:
            child.parent = self
    
    def accept(self, expected):
        if not issubclass(self.__class__, expected):
            raise Exception('Expected %s, instead found %s'
                % (expected, self.__class__.__name__))
        return self
    
    def __iter__(self):
        return iter(self.children)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def to_c(self):
        raise NotImplementedError


