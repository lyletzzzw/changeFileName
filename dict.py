#! /usr/bin/env python
#coding=utf-8

class DictMixin(object):
    """Implement the dict API using keys() and __*item__ methods.

    Similar to UserDict.DictMixin, this takes a class that defines
    __getitem__, __setitem__, __delitem__, and keys(), and turns it
    into a full dict-like object.

    UserDict.DictMixin is not suitable for this purpose because it's
    an old-style class.

    This class is not optimized for very large dictionaries; many
    functions have linear memory requirements. I recommend you
    override some of these functions if speed is required.
    """

    def __iter__(self):
        '''
            返回一个listiterator，使用：
            tmp = iter(dict)
            tmp.next()
        '''
        return iter(self.keys())

    def has_key(self, key):
        '''
            判断参数key是否存在于该字典中
        '''
        try: self[key]
        except KeyError: return False
        else: return True
    __contains__ = has_key

    iterkeys = lambda self: iter(self.keys())

    def values(self):
        '''
            获取字典中所有的值
        '''
        return map(self.__getitem__, self.keys())
    itervalues = lambda self: iter(self.values())

    def items(self):
        '''
            获取字典的所有项
        '''
        return zip(self.keys(), self.values())
    iteritems = lambda s: iter(s.items())

    def clear(self):
        '''
            清空字典中的项
        '''
        map(self.__delitem__, self.keys())

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError("pop takes at most two arguments")
        try: value = self[key]
        except KeyError:
            if args: return args[0]
            else: raise
        del(self[key])
        return value

    def popitem(self):
        try:
            key = self.keys()[0]
            return key, self.pop(key)
        except IndexError: raise KeyError("dictionary is empty")

    def update(self, other=None, **kwargs):
        '''
            更新字典项，使用：
                a = {'a': 1, 'b':2}
                c = {'c':3}
                a.update(c)
            a的结果：
                {'a': 1, 'c': 3, 'b': 2}
        '''
        if other is None:
            self.update(kwargs)
            other = {}

        try: map(self.__setitem__, other.keys(), other.values())
        except AttributeError:
            for key, value in other:
                self[key] = value

    def setdefault(self, key, default=None):
        try: return self[key]
        except KeyError:
            self[key] = default
            return default

    def get(self, key, default=None):
        '''
            根据key获取字典的中该key的值
        '''
        try: return self[key]
        except KeyError: return default

    def __repr__(self):
        return repr(dict(self.items()))

    def __cmp__(self, other):
        if other is None: return 1
        else: return cmp(dict(self.items()), other)

    __hash__ = object.__hash__

    def __len__(self):
        '''
            获取字典的长度
        '''
        return len(self.keys())


class Dict(DictMixin):
    uses_mmap = False

    def __init__(self):
        self.__d = {}
        self.keys = self.__d.keys

    def __getitem__(self, *args): 
        '''
            获取字典中的值，例如：
            print dict['age']
        '''
        return self.__d.__getitem__(*args)
    
    def __setitem__(self, *args):
        '''
            对字典赋值，例如：
            dict['age']=age
        ''' 
        return self.__d.__setitem__(*args)
    
    def __delitem__(self, *args): 
        '''
            删除字典项，例如
            del dict['title']
        '''
        return self.__d.__delitem__(*args)




if __name__=='__main__':
    print 'test'
    
    dict = Dict()
    dict['title']='lyle'
    dict['age']=26
    
    print dict.has_key('title')
    print dict.items()
    

