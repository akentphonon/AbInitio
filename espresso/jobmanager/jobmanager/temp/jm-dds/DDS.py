# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Create a "distributed data storage"
DDS doesn't actually do much without implementation of functions such as:
masternode(), transferfile() etc...
"""

## ***************** Auxiliary functions *****************
#
#def _url1(nodestr,path):
#    return '%s/%s' % (nodestr, path)
#
#
#def _url(node,path):
#    if node.address:
#        return '%s:%s/%s' % (node.address, node.rootpath, path)
#    else:
#        return '%s/%s' % (node.rootpath, path)
#
#
#def _str(node):
#    if node.address:
#        return '%s:%s' % (node.address, node.rootpath)
#    return node.rootpath
#
#
#def _node(s):
#    words = s.split(':')
#    from Node import Node
#    if len(words) == 1: return Node('', s)
#    if len(words) == 2: return Node(words[0], words[1])
#    raise ValueError, "not a node: %s" % (s,)


import os


class DDS:
    def __init__(self,
                 masternode,
                 transferfile   =None,
                 readfile       =None,
                 writefile      =None,
                 makedirs       =None,
                 rename         =None,
                 symlink        =None,
                 fileexists     =None):

        """
        masternode:     a "distributed data storage" must have a master node
        transferfile:   the facility to transfer a file from one node to another
        rename:         the facility to rename a file in one node. rename(oldpath, newpath, "server.address")
        symlink:        the facility to create a symbolic link to a file in one node. symlink(oldpath, newpath, "server.address")
        readfile:       the facility to read a text file. readfile("server.address:/a/b/c")
        writefile:      the facility to write a text file. writefile("server.address:/a/b/c", "contents")
        makedirs:       the facility to make a directory. it should be able to make the intermediate directories automatically
        fileexists:     the facility to check if a file exists on a node or not. fileexists("server.address:/a/b/c")
        """

        self.masternode     = masternode
        self.nodes          = [masternode]
        self._transferfile  = transferfile
        self._readfile      = readfile
        self._writefile     = writefile
        self._makedirs      = makedirs
        self._fileexists    = fileexists
        self._rename        = rename
        self._symlink       = symlink
        return
#
#    def add_node(self, node):
#        """Adds node to the node list"""
#        self.nodes.append(node)
#        return
#
#    def abspath(self, path, node=None):
#        """Returns absolute path: rootpath/path """
#        if node is None:
#            node = self.masternode
#        return os.path.join(node.rootpath, path)
#
#    def rename(self, old, new, node=None):
#        """ """
#        if node is None: node = self.masternode
#        oldpath = '%s/%s' % (node.rootpath, old)
#        newpath = '%s/%s' % (node.rootpath, new)
#        d = os.path.split(new)[0]
#        self._makedirs(_url(node,d))
#        self._rename(oldpath, newpath, node.address)
#        self.forget(old, node)
#        self.remember(new, node)
#        return
#
#
#    def copy(self, old, new, node=None):
#        """ """
#        if node is None: node = self.masternode
#        oldpath = '%s/%s' % (node.rootpath, old)
#        newpath = '%s/%s' % (node.rootpath, new)
#        d = os.path.split(new)[0]
#        self._makedirs(_url(node,d))
#
#        self._transferfile(_url(node,old), _url(node,new))
#
#        self.remember(new, node)
#        return
#
#
## it looks a bad idea to have symlink because it is hard to maintain across nodes
###     def symlink(self, old, new, node=None):
###         if node is None: node = self.masternode
###         oldpath = '%s/%s' % (node.rootpath, old)
###         newpath = '%s/%s' % (node.rootpath, new)
###         d = os.path.split(new)[0]
###         self._makedirs(_url(node,d))
###         self._symlink(oldpath, newpath, node.address)
###         self.remember(new, node)
###         return
#
#
#    def remember(self, path, node=None):
#        """Remembers that a path of a node exists
#
#        node: the node that the path exists. None means master node
#        path: the path
#        """
#        if node is None: node = self.masternode
#        url = _url(node,path)
#        if not self._fileexists(url):
#            raise RuntimeError, "url %s does not exist" % url
#
#        l = self._read_availability_list(path)
#        s = _str(node)
#        if s not in l: l.append(s)
#
#        self._update_availability_list(path, l)
#        return
#
#
#    def forget(self, path, node=None):
#        """ """
#        if node is None: node = self.masternode
#        url = _url(node,path)
#        if self._fileexists(url):
#            raise RuntimeError, "url %s still exists" % url
#
#        l = self._read_availability_list(path)
#        s = _str(node)
#        if s in l: del l[l.index(s)]
#
#        self._update_availability_list(path, l)
#        return
#
#
#
#    def is_available(self, path, node=None):
#        """ """
#        if node is None: node = self.masternode
#
#        l = self._read_availability_list(path)
#        if _str(node) in l: return True
#
#        ret = self._fileexists(_url(node, path))
#        if ret:
#            l.append(_str(node))
#            self._update_availability_list(path,l)
#        return ret
#
#
#    def make_available(self, path, node=None):
#        """ """
#        '''make file at given path available at given node'''
#        if self.is_available(path, node): return
#        if node is None: node = self.masternode
#        node1 = self.find_node(path)
#        if node1 is None: raise RuntimeError, "%s is not available anywhere" % path
#        self._transfer(path, node1, node)
#        self.remember(path, node)
#        return
#
#
#    def find_node(self, path):
#        '''find the node which has the file whose path is given'''
#        l = self._read_availability_list(path)
#        expired = []; ret = None
#        for n in l:
#            if not self._fileexists(_url1(n,path)): expired.append(n)
#            else: ret = n; break
#            continue
#        if expired:
#            l1 = filter(lambda n: n not in expired, l)
#            self._update_availability_list(path, l1)
#        if ret is None: raise RuntimeError, "no node has the path %r" % path
#        return _node(ret)
#
#
#    def _transfer(self, path, srcnode, destnode):
#        """ """
#        d = os.path.split(path)[0]
#        self._makedirs(_url(destnode,d))
#        return self._transferfile(_url(srcnode,path), _url(destnode,path))
#
#
#    def _read_availability_list(self, path):
#        """ """
#        p = self._availability_list_path(path)
#        if self._fileexists(p):
#            return self._readfile(p).split('\n')
#        return []
#
#    def _update_availability_list(self, path, list):
#        """ """
#        p = self._availability_list_path(path)
#        d = os.path.split(p)[0]
#        self._makedirs(d)
#        return self._writefile(p, '\n'.join(list))
#
#    ext_remember='__dds_nodelist'
#    prefix_remember='.__dds_nodelist'
#    def _availability_list_path(self, path):
#        masternode = self.masternode
#        d, p = os.path.split(path)
#        newpath = os.path.join(d, '%s.%s.%s' % (self.prefix_remember, p, self.ext_remember))
#        url = _url(masternode, newpath)
#        return url
#
#    pass # end of DDS
#
#
#
#
#
#
#
#
#
## ***************** Tests *****************
#
#def test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, fileexists):
#    import os, shutil
#
#    import os
#    dds = DDS(masternode, transferfile=transferfile,
#              readfile=readfile, writefile=writefile, makedirs=makedirs,
#              rename=rename, symlink=symlink, fileexists=fileexists)
#    if os.path.exists(masternode.rootpath): shutil.rmtree(masternode.rootpath)
#    try:
#        dds.remember('file1')
#    except RuntimeError:
#        pass
#    else: raise Exception, "should have raised RuntimeError"
#
#    os.makedirs(masternode.rootpath)
#    open(os.path.join(masternode.rootpath, 'file1'), 'w').write('')
#
#    import time
#    time.sleep(0.1)
#    dds.remember('file1')
#
#    dds.add_node(node1)
#    if os.path.exists(node1.rootpath): shutil.rmtree(node1.rootpath)
#    dds.make_available('file1', node1)
#    assert os.path.exists(os.path.join(node1.rootpath,'file1'))
#    assert dds.is_available('file1', node1)
#
#    open(os.path.join(node1.rootpath, 'file2'), 'w').write('file2')
#    dds.remember('file2', node1)
#    dds.make_available('file2')
#    assert os.path.exists(os.path.join(masternode.rootpath,'file2'))
#    assert dds.is_available('file2', masternode)
#
#    dds.rename('file2', 'file3')
#    assert not dds.is_available('file2')
#    assert dds.is_available('file3')
#
##    dds.symlink('file3', 'file4')
##    assert dds.is_available('file4')
#    return
#
#
#def test1():
#    import os
#    from Node import Node
#    masternode = Node( '', os.path.abspath('masternode') )
#    node1 = Node( '', os.path.abspath('node1') )
#
#    import os, shutil
#    def transferfile(path1, path2):
#        shutil.copyfile(path1, path2)
#        return
#
#    def readfile(path):
#        return open(path).read()
#
#    def writefile(path, content):
#        open(path, 'w').write(content)
#        return
#
#    def makedirs(path):
#        if os.path.exists(path): return
#        os.makedirs(path)
#        return
#
#    def rename(path1, path2, dummy):
#        os.rename(path1, path2)
#        return
#
#    def symlink(path1, path2, dummy):
#        os.symlink(path1, path2)
#        return
#
#    test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, os.path.exists)
#    return
#
#
#def test2():
#    from Node import Node
#    import os
#    curdir = os.path.abspath('.')
#    masternode = Node( 'localhost', os.path.join(curdir,'masternode'))
#    node1 = Node( 'localhost', os.path.join(curdir,'node1') )
#
#    import os, shutil
#    def transferfile(path1, path2):
#        cmd = 'scp %s %s' % (path1,path2)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def readfile(path):
#        path = path.split(':')[1]
#        return open(path).read()
#
#    def writefile(path, content):
#        path = path.split(':')[1]
#        open(path, 'w').write(content)
#        return
#
#    def makedirs(path):
#        path = path.split(':')[1]
#        if os.path.exists(path): return
#        os.makedirs(path)
#        return
#
#    def rename(path1, path2, host):
#        cmd = 'ssh %s mv %s %s' % (host, path1, path2)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def symlink(path1, path2, host):
#        cmd = 'ssh %s ln -s %s %s' % (host, path1, path2)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def fileexists(path):
#        path = path.split(':')[1]
#        return os.path.exists(path)
#
#    test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, fileexists)
#    return
#
## Tests file operations with remote server
#
#def testRemote():
#    import os
#    import shutil
#    from Node import Node
#
#    curdir = "/home/dexity/"
#    masternode = Node( 'dexity@foxtrot.danse.us', os.path.join(curdir, 'masternode'))
#
#    def transferfile(path1, path2):
#        cmd = 'scp %s %s' % (path1,path2)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def readfile(path):
#        path = path.split(':')[1]
#        return open(path).read()
#
#    def writefile(host, path, content):
#        cmd = """ssh %s 'echo "%s" > %s'""" % (host, content, path)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def makedirs(host, path):
#        cmd = """ssh %s 'dir="%s"; if [ ! -d $dir ]; then mkdir $dir; fi'""" % (host, path)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def rename(path1, path2, host):
#        cmd = 'ssh %s mv %s %s' % (host, path1, path2)
#        print 'executing %s...' % cmd
#        code = os.system(cmd)
#        print 'returned %s' % code
#        if code: raise RuntimeError
#        return
#
#    def fileexists(path):
#        path = path.split(':')[1]
#        return os.path.exists(path)
#
#    testMasterNode(masternode, transferfile, readfile, writefile, makedirs, rename, fileexists)
#    return
#
## Tests file operations with local file system
#
#def testLocal():
#    import os
#    from Node import Node
#    masternode = Node( '', os.path.abspath('masternode') )
#
#    def transferfile(path1, path2):
#        shutil.copyfile(path1, path2)
#        return
#
#    def readfile(path):
#        return open(path).read()
#
#    def writefile(path, content):
#        open(path, 'w').write(content)
#        return
#
#    def makedirs(path):
#        if os.path.exists(path): return
#        os.makedirs(path)
#        return
#
#    def rename(path1, path2, dummy):
#        os.rename(path1, path2)
#        return
#
#    testMasterNode(masternode, transferfile, readfile, writefile, makedirs, rename, os.path.exists)
#    return
#
#
#def testMasterNode(masternode, transferfile, readfile, writefile, makedirs, rename, fileexists):
#    fn1         = "file1"
#    fn2         = "file2"
#    fn3         = "file3"
#
#    import shutil
#    import os
#    dds = DDS(masternode, transferfile=transferfile,
#              readfile=readfile, writefile=writefile, makedirs=makedirs,
#              rename=rename, fileexists=fileexists)
#    if os.path.exists(masternode.rootpath): shutil.rmtree(masternode.rootpath)
#    try:
#        dds.remember(fn1)
#    except RuntimeError:
#        pass
#    else: raise Exception, "should have raised RuntimeError"
#
#    makedirs(masternode.address, masternode.rootpath)
#    writefile(masternode.address, os.path.join(masternode.rootpath, fn1), 'blah')
#
## Not sure is the underlying lines work, but the idea is clear :)
#
##    import time
##    time.sleep(0.1)
##    dds.remember(fn1)
##
##    dds.make_available(fn1, masternode)
##    assert os.path.exists(os.path.join(masternode.rootpath, fn1))
##    assert dds.is_available(fn1, masternode)
##
##    open(os.path.join(masternode.rootpath, fn2), 'w').write('file2')
##    dds.remember(fn2, masternode)
##    dds.make_available(fn2)
##    assert os.path.exists(os.path.join(masternode.rootpath,fn2))
##    assert dds.is_available(fn2, masternode)
##
##    dds.rename(fn2, fn3, masternode)
##    assert not dds.is_available(fn2)
##    assert dds.is_available(fn3)
#
#    return
#
#def main():
#    #testLocal()
#    testRemote()
#
#    # Old tests
#    #test1()
#    #test2()
#    return
#
#
#if __name__ == '__main__':
#    main()


# version
__id__ = "$Id$"

# End of file 
